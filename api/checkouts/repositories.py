from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.checkouts.models import Checkout


async def get_checkout(db: AsyncSession, checkout_id: UUID) -> Checkout | None:
    result = await db.execute(select(Checkout).where(Checkout.id == checkout_id))
    return result.scalars().first()


async def get_checkout_by_cart(db: AsyncSession, cart_id: UUID) -> Checkout | None:
    result = await db.execute(select(Checkout).where(Checkout.cart_id == cart_id))
    return result.scalars().first()


async def create_checkout(
    db: AsyncSession,
    cart_id: UUID,
    customer_id: UUID,
    total_amount: Decimal,
) -> Checkout:
    checkout = Checkout(
        cart_id=cart_id,
        customer_id=customer_id,
        total_amount=total_amount,
    )
    db.add(checkout)
    await db.flush()
    await db.refresh(checkout)
    return checkout
