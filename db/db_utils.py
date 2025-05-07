from sqlalchemy.ext.asyncio import AsyncSession

from db.model.budget import Budget
from db.model.date import Date
from db.model.interests import Interest
from db.model.notifications import Notifications
from db.model.place import Place
from db.model.task import Task


class BudgetModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def budget_add(
        self, chat_id, min_cost, max_cost
    ) -> Budget:
        budget = Budget(chat_id=chat_id, min_cost=min_cost, max_cost=max_cost)
        self.session.add(budget)
        await self.session.commit()
        return budget


class DateModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def date_add(self, chat_id, with_dates,end_dates) -> Date:
        date = Date(chat_id=chat_id, with_dates=with_dates, end_dates=end_dates)
        self.session.add(date)
        await self.session.commit()
        return date


class InterestModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def interest_add(self, chat_id, pref) -> Interest:
        interest = Date(chat_id=chat_id, pref=pref)
        self.session.add(interest)
        await self.session.commit()
        return interest


class NotificationsModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def notific_add(self, chat_id, date, text) -> Notifications:
        notific = Date(chat_id=chat_id, date=date, text=text)
        self.session.add(notific)
        await self.session.commit
        return notific


class PlaceModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def place_add(self, chat_id, white_list, black_list) -> Place:
        place = Place(chat_id=chat_id, white_list=white_list, black_list=black_list)
        self.session.add(place)
        await self.session.commit
        return place

class TaskModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def task_add(self, chat_id, user_id, target):
        task = Task(chat_id=chat_id,user_id=user_id, target=target)
        self.session.add(task)
        await self.session.commit
        return task
