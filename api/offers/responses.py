from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OfferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    customer_id: UUID
    unit_price: Decimal
    validity: date
    created_at: datetime
    updated_at: datetime
