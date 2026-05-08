from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.carts.payloads import CartItemAddPayload
from api.carts.responses import CartResponse
from api.carts.services import add_item, get_cart, remove_item
from api.storage.postgresql import get_db

router = APIRouter()


@router.get("/{customer_id}", response_model=CartResponse)
async def get_customer_cart(
    customer_id: UUID, db: AsyncSession = Depends(get_db)
) -> CartResponse:
    return await get_cart(db, customer_id)


@router.post("/{customer_id}/items", response_model=CartResponse)
async def add_cart_item(
    customer_id: UUID,
    payload: CartItemAddPayload,
    db: AsyncSession = Depends(get_db),
) -> CartResponse:
    return await add_item(db, customer_id, payload.offer_id, payload.quantity)


@router.delete("/{customer_id}/items/{offer_id}", response_model=CartResponse)
async def delete_cart_item(
    customer_id: UUID,
    offer_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> CartResponse:
    return await remove_item(db, customer_id, offer_id)
