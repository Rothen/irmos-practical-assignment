from sqlalchemy import Float, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Midspan(Base):
    __tablename__ = "midspan"

    time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    Fat_cycle_bot: Mapped[float] = mapped_column(Float)
    Pos_na: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f"Midspan(time={self.time!r}, Fat_cycle_bot={self.Fat_cycle_bot!r}, Pos_na={self.Pos_na!r})"