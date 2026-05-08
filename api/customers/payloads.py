from pydantic import BaseModel, Field, field_validator


class CustomerCreatePayload(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    cnpj: str = Field(min_length=12, max_length=18)

    @field_validator("cnpj")
    @classmethod
    def normalize_cnpj(cls, value: str) -> str:
        normalized = "".join(ch for ch in value if ch.isalnum()).upper()
        if len(normalized) != 14:
            raise ValueError("CNPJ must have 14 alphanumeric characters")
        return normalized
