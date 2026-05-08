from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.carts.models import CartStatus, CartItem
from api.carts.repositories import get_cart_by_id
from api.checkouts.models import Checkout, CheckoutStatus
from api.checkouts.repositories import (
    create_checkout,
    get_checkout,
    get_checkout_by_cart,
)
from api.offers.models import Offer


async def create_checkout_from_cart(db: AsyncSession, cart_id: UUID) -> Checkout:
    cart = await get_cart_by_id(db=db, cart_id=cart_id, with_items=False)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if cart.status != CartStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is not open",
        )

    existing = await get_checkout_by_cart(db=db, cart_id=cart_id)
    if existing:
        return existing

    result = await db.execute(
        select(CartItem, Offer)
        .join(Offer, CartItem.offer_id == Offer.id)
        .where(CartItem.cart_id == cart_id)
    )
    rows: list[tuple[CartItem, Offer]] = result.all()
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )

    total = Decimal("0.00")
    for item, offer in rows:
        total += Decimal(item.quantity) * Decimal(offer.unit_price)

    total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    checkout = await create_checkout(
        db=db, cart_id=cart_id, customer_id=cart.customer_id, total_amount=total
    )
    cart.status = CartStatus.CHECKOUT
    await db.flush()
    return checkout


async def pay_checkout(db: AsyncSession, checkout_id: UUID) -> Checkout:
    checkout = await get_checkout(db=db, checkout_id=checkout_id)
    if not checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Checkout not found"
        )
    if checkout.status != CheckoutStatus.PENDING_PAYMENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Checkout already paid",
        )

    cart = await get_cart_by_id(db=db, cart_id=checkout.cart_id, with_items=False)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    now = datetime.now(timezone.utc)
    checkout.status = CheckoutStatus.PAID
    checkout.paid_at = now
    cart.status = CartStatus.PAID
    cart.checked_out_at = now
    await db.flush()
    await db.refresh(checkout)
    return checkout
