CREATE TABLE IF NOT EXISTS telemetry (
    telemetry_id SERIAL PRIMARY KEY,
    timestamp DOUBLE PRECISION,
    robot_x FLOAT,
    robot_y FLOAT,
    linear_x FLOAT,
    angular_z FLOAT,
    front_clearance FLOAT,
    state TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS detection_events (
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
