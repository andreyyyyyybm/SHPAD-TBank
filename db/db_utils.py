from sqlalchemy.ext.asyncio import AsyncSession

from db.model.budget import Budget


class BudgetModel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def budget_add(self, chat_id: int, min_cost: int, max_cost: int) -> Budget:
        budget = Budget(chat_id=chat_id, min_cost=min_cost, max_cost=max_cost)
        self.session.add(budget)
        await self.session.commit()
        return budget
    
