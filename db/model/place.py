from sqlalchemy import Column, Integer, String

from db.database import Base


class Place(Base):
    __tablename__ = "place"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    white_list = Column(String)
    black_list = Column(String)
