import os


def test_schema_sql_exists():
    schema_path = os.path.join("sql", "schema.sql")
    assert os.path.exists(schema_path)

    with open(schema_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    assert "CREATE TABLE" in sql_content
    assert "telemetry" in sql_content.lower() or "navigation" in sql_content.lower()
