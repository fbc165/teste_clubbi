from uuid import UUID

from pydantic import BaseModel


class CheckoutCreatePayload(BaseModel):
    cart_id: UUID
