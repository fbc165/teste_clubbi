from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class OfferCreatePayload(BaseModel):
    product_id: UUID
    customer_id: UUID
    unit_price: Decimal = Field(gt=0, decimal_places=2)
    validity: date

    @field_validator("validity")
    @classmethod
    def validate_validity(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Validity must be today or in the future")
        return value
