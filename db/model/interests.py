from sqlalchemy import Column, Integer, String
from db.database import Base


class Interest(Base):
    __tablename__ = "interest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    pref = Column(String)
