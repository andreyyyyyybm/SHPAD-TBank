from sqlalchemy import Column, Integer, Date
from db.database import Base


class Date(Base):
    __tablename__ = "date"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    with_dates = Column(Date)
    end_dates = Column(Date)
