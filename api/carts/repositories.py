from datetime import date
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.carts.models import Cart, CartItem, CartStatus
from api.offers.models import Offer


async def get_open_cart(
    db: AsyncSession, customer_id: UUID, with_items: bool = True
) -> Cart | None:
    query = select(Cart).where(
        Cart.customer_id == customer_id, Cart.status == CartStatus.OPEN
    )
    if with_items:
        query = query.options(selectinload(Cart.items))
    result = await db.execute(query)
    return result.scalars().first()


async def create_cart(db: AsyncSession, customer_id: UUID) -> Cart:
    cart = Cart(customer_id=customer_id)
    db.add(cart)
    await db.flush()
    await db.refresh(cart)
    return cart


async def get_cart_by_id(
    db: AsyncSession, cart_id: UUID, with_items: bool = True
) -> Cart | None:
    query = select(Cart).where(Cart.id == cart_id)
    if with_items:
        query = query.options(selectinload(Cart.items))
    result = await db.execute(query)
    return result.scalars().first()


async def get_valid_offer(
    db: AsyncSession, customer_id: UUID, offer_id: UUID
) -> Offer | None:
    result = await db.execute(
        select(Offer).where(
            Offer.id == offer_id,
            Offer.customer_id == customer_id,
            Offer.validity >= date.today(),
        )
    )
    return result.scalars().first()


async def get_cart_item(
    db: AsyncSession, cart_id: UUID, offer_id: UUID
) -> CartItem | None:
    result = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart_id, CartItem.offer_id == offer_id
        )
    )
    return result.scalars().first()


async def upsert_cart_item(
    db: AsyncSession, cart_id: UUID, offer_id: UUID, quantity: int
) -> CartItem:
    item = await get_cart_item(db, cart_id, offer_id)
    if item:
        item.quantity += quantity
        await db.flush()
        return item

    item = CartItem(cart_id=cart_id, offer_id=offer_id, quantity=quantity)
    db.add(item)
    await db.flush()
    return item


async def delete_cart_item(
    db: AsyncSession, cart_id: UUID, offer_id: UUID
) -> int:
    result = await db.execute(
        delete(CartItem).where(
            CartItem.cart_id == cart_id, CartItem.offer_id == offer_id
        )
    )
    return result.rowcount or 0
