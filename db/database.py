import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)


class Database:
    def __init__(
        self,
    ):
        self.engine = engine
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # async def add_budget(self, chat_id, min_cost, max_cost):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             bud = Budget(
    #                 chat_id=chat_id, min_cost=min_cost, max_cost=max_cost
    #             )
    #             session.add(bud)
    #         await session.commit()

    # async def add_date(self, chat_id, with_dates, end_dates):
    #     async with self.async_session() as session:
    #         async with session.begin():
    #             date = Date(
    #                 chat_id=chat_id, with_dates=with_dates, end_dates=end_dates
    #             )
    #             session.add(date)
    #         await session.commit
    async def get_session(self) -> AsyncSession:
        return self.async_session()

    async def close(self):
        await self.engine.dispose()
