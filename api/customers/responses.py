from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str
    cnpj: str
    created_at: datetime
    updated_at: datetime
