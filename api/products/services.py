from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from api.products.models import Product
from api.products.repositories import list_products


async def get_products(db: AsyncSession) -> Sequence[Product]:
    return await list_products(db)
