import sys

import psycopg2

query_label = sys.argv[1] if len(sys.argv) > 1 else "suitcase"

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="semantic_map",
    user="postgres",
    password="postgres",
)
cur = conn.cursor()

cur.execute(
    """
SELECT
    p.place_id,
    p.place_label,
    COUNT(*) AS matches,
    MAX(o.confidence) AS best_confidence
FROM object_observations o
JOIN places p ON o.place_id = p.place_id
WHERE lower(o.object_class) = lower(%s)
GROUP BY p.place_id, p.place_label
ORDER BY matches DESC, best_confidence DESC
LIMIT 3;
""",
    (query_label,),
)

rows = cur.fetchall()

print(f"Top 3 candidate places for query label: {query_label}")
for r in rows:
    print(
        {
            "place_id": r[0],
            "place_label": r[1],
            "matches": r[2],
            "best_confidence": float(r[3]) if r[3] is not None else None,
        }
    )

cur.close()
conn.close()
