import psycopg
from psycopg.rows import dict_row
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="Example API", version="1.0.0")

database_url = "postgresql://irmos:pwd123@db:5432/actual_bridge"

@app.get("/bridge-data")
def bridge_data() -> dict:
    sql = """
        SELECT time, "Fat_cycle_bot", "Pos_na"
        FROM midspan
        ORDER BY time ASC
    """
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    if not rows:
        return {"_time": [], "stress_cycle": [], "pos_na": []}

    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
    df.rename(columns={"Fat_cycle_bot": "stress_cycle", "Pos_na": "pos_na"}, inplace=True)
    df = df.set_index("time").sort_index()
    df = df[["stress_cycle", "pos_na"]].apply(pd.to_numeric, errors="coerce")

    def drop_outliers_mad(s: pd.Series, k: float = 3.5) -> pd.Series:
        med = s.median()
        mad = (s - med).abs().median()
        if mad == 0 or pd.isna(mad):
            return s
        rzs = 1.4826 * (s - med).abs() / mad
        return s.where(rzs <= k)

    for col in ["stress_cycle", "pos_na"]:
        df[col] = drop_outliers_mad(df[col], 3.5)

    df = df.dropna(how="all")  # drop rows where both values were outliers/NaN

    if df.empty:
        return {"_time": [], "stress_cycle": [], "pos_na": []}

    ds = df.resample("150min").mean(numeric_only=True)

    sm = ds.rolling("500min", min_periods=1).mean()

    times = sm.index.strftime("%Y-%m-%dT%H:%M:%S.%f%z").str.replace("+0000", "Z").tolist()
    stress = sm["stress_cycle"].where(pd.notna(sm["stress_cycle"]), None).tolist()
    posna = sm["pos_na"].where(pd.notna(sm["pos_na"]), None).tolist()

    return {"_time": times, "stress_cycle": stress, "pos_na": posna}