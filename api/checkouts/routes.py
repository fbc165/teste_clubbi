from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.checkouts.payloads import CheckoutCreatePayload
from api.checkouts.responses import CheckoutResponse
from api.checkouts.services import create_checkout_from_cart, pay_checkout
from api.storage.postgresql import get_db

router = APIRouter()


@router.post("", response_model=CheckoutResponse)
async def create_checkout(
    payload: CheckoutCreatePayload, db: AsyncSession = Depends(get_db)
) -> CheckoutResponse:
    return await create_checkout_from_cart(db, payload.cart_id)


@router.post("/{checkout_id}/pay", response_model=CheckoutResponse)
async def pay_checkout_endpoint(
    checkout_id: UUID, db: AsyncSession = Depends(get_db)
) -> CheckoutResponse:
    return await pay_checkout(db, checkout_id)
