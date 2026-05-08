from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.products.models import Product


async def list_products(db: AsyncSession) -> Sequence[Product]:
    result = await db.execute(select(Product).order_by(Product.name))
    return result.scalars().all()
