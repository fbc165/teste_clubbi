from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.customers.responses import CustomerResponse
from api.customers.services import get_customers
from api.storage.postgresql import get_db

router = APIRouter()


@router.get("", response_model=list[CustomerResponse])
async def list_customers(db: AsyncSession = Depends(get_db)) -> Sequence[CustomerResponse]:
    return await get_customers(db)
