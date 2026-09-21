import time

import psycopg2

conn = psycopg2.connect(
    dbname="maze",
    user="root",
)

cur = conn.cursor()

print("Zenoh ingest worker started")

while True:
    cur.execute("""
        INSERT INTO detection_events
        (event_id, run_id, robot_id, timestamp, class, confidence, x, y, width, height)
        VALUES ('test123','run001','tb3_sim',NOW(),'cone',0.92,0.5,0.4,0.2,0.3)
    """)

    conn.commit()

    print("Inserted event into PostgreSQL")

    time.sleep(5)
