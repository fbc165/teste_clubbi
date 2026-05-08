from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from api.customers.models import Customer
from api.customers.repositories import list_customers


async def get_customers(db: AsyncSession) -> Sequence[Customer]:
    return await list_customers(db)
