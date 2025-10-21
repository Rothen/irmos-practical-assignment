from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row

app = FastAPI(title="Example API", version="1.0.0")

database_url = "postgresql://irmos:pwd123@db:5432/actual_bridge"

@app.get("/midspan")
def midspan():
    
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM midspan;")
            rows = cur.fetchall()
        
    return {
        "status": "ok",
        "data": rows
    }