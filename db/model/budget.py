from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base


class Budget(Base)
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    min_cost = Column(Integer)
    max_cost = Column(Integer) 