from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ean: str
    name: str
    items_per_box: int
    created_at: datetime
    updated_at: datetime
