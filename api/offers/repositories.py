from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.offers.models import Offer


async def list_offers_by_customer(
    db: AsyncSession, customer_id: UUID
) -> Sequence[Offer]:
    result = await db.execute(
        select(Offer)
        .where(Offer.customer_id == customer_id)
        .order_by(Offer.validity.desc())
    )
    return result.scalars().all()
