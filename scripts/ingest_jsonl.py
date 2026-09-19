import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="semantic_map",
    user="postgres",
    password="postgres",
)
cur = conn.cursor()

# Load detections
with open("detections.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        cur.execute(
            "INSERT INTO detections (raw_json) VALUES (%s::jsonb)",
            (line,)
        )

# Load poses
with open("slam.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        cur.execute(
            "INSERT INTO slam_poses (raw_json) VALUES (%s::jsonb)",
            (line,)
        )

conn.commit()
cur.close()
conn.close()

print("Done loading detections and slam poses.")
