from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.offers.responses import OfferResponse
from api.offers.services import get_offers_by_customer
from api.storage.postgresql import get_db

router = APIRouter()


@router.get("", response_model=list[OfferResponse])
async def list_offers(
    customer_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> Sequence[OfferResponse]:
    return await get_offers_by_customer(db, customer_id)
