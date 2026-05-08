from __future__ import annotations

import asyncio
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select

from api.customers.models import Customer
from api.offers.models import Offer
from api.products.models import Product
from api.storage.postgresql.session import Session


def normalize_cnpj(value: str) -> str:
    return "".join(ch for ch in value if ch.isalnum()).upper()


async def get_or_create_customer(db, name: str, address: str, cnpj: str) -> Customer:
    normalized = normalize_cnpj(cnpj)
    result = await db.execute(select(Customer).where(Customer.cnpj == normalized))
    customer = result.scalars().first()
    if customer:
        return customer
    customer = Customer(name=name, address=address, cnpj=normalized)
    db.add(customer)
    await db.flush()
    return customer


async def get_or_create_product(db, ean: str, name: str, items_per_box: int) -> Product:
    result = await db.execute(select(Product).where(Product.ean == ean))
    product = result.scalars().first()
    if product:
        return product
    product = Product(ean=ean, name=name, items_per_box=items_per_box)
    db.add(product)
    await db.flush()
    return product


async def create_offer(
    db, customer_id, product_id, unit_price: Decimal, validity: date
) -> Offer:
    offer = Offer(
        customer_id=customer_id,
        product_id=product_id,
        unit_price=unit_price,
        validity=validity,
    )
    db.add(offer)
    await db.flush()
    return offer


async def seed() -> None:
    async with Session() as db:
        customer_a = await get_or_create_customer(
            db, "Loja Alpha", "Rua Um, 100", "12.345.678/0001-90"
        )
        customer_b = await get_or_create_customer(
            db, "Mercado Beta", "Av. Dois, 200", "98.765.432/0001-10"
        )

        product_a = await get_or_create_product(db, "7891234567890", "Cafe", 12)
        product_b = await get_or_create_product(db, "7899876543210", "Arroz", 30)

        await create_offer(
            db,
            customer_a.id,
            product_a.id,
            Decimal("12.90"),
            date.today() + timedelta(days=30),
        )
        await create_offer(
            db,
            customer_a.id,
            product_b.id,
            Decimal("19.50"),
            date.today() + timedelta(days=30),
        )
        await create_offer(
            db,
            customer_b.id,
            product_a.id,
            Decimal("11.75"),
            date.today() + timedelta(days=15),
        )

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
