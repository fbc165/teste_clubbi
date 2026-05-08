from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.customers.models import Customer


async def list_customers(db: AsyncSession) -> Sequence[Customer]:
    result = await db.execute(select(Customer).order_by(Customer.name))
    return result.scalars().all()
