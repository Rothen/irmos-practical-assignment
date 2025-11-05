"""Resources for the cameras API"""
from typing import TypedDict
from singleton import Singleton
import pandas as pd
from typing import TypedDict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from midspan import Midspan

database_url = "postgresql://irmos:pwd123@db:5432/actual_bridge"

class BridgeData(TypedDict):
    _time: list[str]
    stress_cycle: list[float | None]
    pos_na: list[float | None]

class BridgeManager(metaclass=Singleton):
    """Singleton class to manage bridge data."""
    
    def __init__(self) -> None:
        self.engine = create_engine(database_url, echo=True)
    
    def _load_bridge_data(self) -> pd.DataFrame:
        """Load bridge data from the database into a pandas DataFrame."""
        session = Session(self.engine)
        stmt = select(Midspan).order_by(Midspan.time.asc())
        df = pd.read_sql(stmt, session.bind)

        df["time"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
        df.rename(columns={"Fat_cycle_bot": "stress_cycle", "Pos_na": "pos_na"}, inplace=True)
        df = df.set_index("time").sort_index()
        df = df[["stress_cycle", "pos_na"]].apply(pd.to_numeric, errors="coerce")

        return df

    def _drop_outliers_mad(self, s: pd.Series, k: float = 3.5) -> pd.Series:
        med = s.median()
        mad = (s - med).abs().median()
        if mad == 0 or pd.isna(mad):
            return s
        rzs = 1.4826 * (s - med).abs() / mad
        return s.where(rzs <= k)
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in ["stress_cycle", "pos_na"]:
            df[col] = self._drop_outliers_mad(df[col], 3.5)

        df = df.dropna(how="all")

        ds = df.resample("150min").mean(numeric_only=True)

        return ds.rolling("500min", min_periods=1).mean()

    def bridge_data(self) -> BridgeData:
        df = self._load_bridge_data()
        sm = self._prepare_data(df)

        times = sm.index.strftime("%Y-%m-%dT%H:%M:%S.%f%z").str.replace("+0000", "Z").tolist()
        stress = sm["stress_cycle"].where(pd.notna(sm["stress_cycle"]), None).tolist()
        posna = sm["pos_na"].where(pd.notna(sm["pos_na"]), None).tolist()

        if sm.empty:
            return {"_time": [], "stress_cycle": [], "pos_na": []}

        return {"_time": times, "stress_cycle": stress, "pos_na": posna}