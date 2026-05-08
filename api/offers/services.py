from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.offers.models import Offer
from api.offers.repositories import list_offers_by_customer


async def get_offers_by_customer(
    db: AsyncSession, customer_id: UUID
) -> Sequence[Offer]:
    return await list_offers_by_customer(db, customer_id)
