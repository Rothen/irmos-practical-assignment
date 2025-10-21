from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import numpy as np

app = FastAPI(title="Example API", version="1.0.0")

database_url = "postgresql://irmos:pwd123@db:5432/actual_bridge"

@app.get("/bridge-data")
def bridge_data() -> dict:
    try:
        with psycopg.connect(database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM midspan;")
                rows = cur.fetchall()
        
        _time = [row['time'] for row in rows]
        stress_cycle = [row['Fat_cycle_bot'] for row in rows]
        pos_na = [row['Pos_na'] for row in rows]
        
        return { 
            "_time": _time,
            "stress_cycle": stress_cycle,
            "pos_na": pos_na,
        }
    except Exception as e:
        return { "status": "error", "message": str(e) }