from uuid import UUID

from pydantic import BaseModel, Field


class CartItemAddPayload(BaseModel):
    offer_id: UUID
    quantity: int = Field(gt=0, le=100000)
