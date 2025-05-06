from sqlalchemy import Column, Integer, DateTime, String
from db.database import Base


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    date = Column(DateTime)
    text = Column(String)
