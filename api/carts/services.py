from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.carts.models import Cart
from api.carts.repositories import (
    create_cart,
    delete_cart_item,
    get_open_cart,
    get_valid_offer,
    upsert_cart_item,
)


async def get_cart(db: AsyncSession, customer_id: UUID) -> Cart:
    cart = await get_open_cart(db, customer_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    return cart


async def add_item(
    db: AsyncSession, customer_id: UUID, offer_id: UUID, quantity: int
) -> Cart:
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantity must be greater than zero",
        )

    offer = await get_valid_offer(db, customer_id, offer_id)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offer is not valid for this customer",
        )

    cart = await get_open_cart(db, customer_id, with_items=False)
    if not cart:
        cart = await create_cart(db, customer_id)

    await upsert_cart_item(db, cart.id, offer_id, quantity)
    cart = await get_open_cart(db, customer_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load cart",
        )
    return cart


async def remove_item(
    db: AsyncSession, customer_id: UUID, offer_id: UUID
) -> Cart:
    cart = await get_open_cart(db, customer_id, with_items=False)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    removed = await delete_cart_item(db, cart.id, offer_id)
    if removed == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    cart = await get_open_cart(db, customer_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load cart",
        )
    return cart
