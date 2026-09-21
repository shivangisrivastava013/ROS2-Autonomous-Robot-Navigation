import psycopg2
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="semantic_map",
    user="postgres",
    password="postgres",
)
cur = conn.cursor()

# Load a small, fast model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Get detections that have non-empty payloads
cur.execute("""
    SELECT det_pk, raw_json
    FROM detections
    WHERE jsonb_array_length(raw_json->'payload') > 0
    ORDER BY det_pk
    LIMIT 100
""")

rows = cur.fetchall()
print(f"Found {len(rows)} detections with non-empty payloads")

inserted = 0

for det_pk, raw_json in rows:
    payload = raw_json.get("payload", [])
    labels = []

    for obj in payload:
        cls = obj.get("class")
        if cls:
            labels.append(cls)

    if not labels:
        continue

    text = " ".join(labels)
    emb = model.encode(text).tolist()

    # pad/truncate to 512 dims for your table schema
    if len(emb) < 512:
        emb = emb + [0.0] * (512 - len(emb))
    elif len(emb) > 512:
        emb = emb[:512]

    vector_literal = "[" + ",".join(str(float(x)) for x in emb) + "]"

    cur.execute(
        """
        INSERT INTO detection_embeddings (det_pk, model, embedding)
        VALUES (%s, %s, %s::vector)
        ON CONFLICT (det_pk) DO NOTHING
    """,
        (det_pk, "all-MiniLM-L6-v2", vector_literal),
    )

    inserted += 1

conn.commit()
print(f"Inserted {inserted} embeddings")

cur.close()
conn.close()
