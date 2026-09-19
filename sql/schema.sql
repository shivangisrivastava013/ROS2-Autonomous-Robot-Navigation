CREATE TABLE detection_events (
    event_id SERIAL PRIMARY KEY,
    run_id TEXT,
    robot_id TEXT,
    timestamp TIMESTAMP,
    class TEXT,
    confidence FLOAT,
    x FLOAT,
    y FLOAT,
    width FLOAT,
    height FLOAT
);
