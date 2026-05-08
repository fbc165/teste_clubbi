from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.products.responses import ProductResponse
from api.products.services import get_products
from api.storage.postgresql import get_db

router = APIRouter()


@router.get("", response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)) -> Sequence[ProductResponse]:
    return await get_products(db)
