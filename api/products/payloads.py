from pydantic import BaseModel, Field, field_validator


class ProductCreatePayload(BaseModel):
    ean: str = Field(min_length=8, max_length=14)
    name: str = Field(min_length=1, max_length=255)
    items_per_box: int = Field(gt=0, le=100000)

    @field_validator("ean")
    @classmethod
    def normalize_ean(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) not in {8, 12, 13, 14}:
            raise ValueError("EAN must have 8, 12, 13, or 14 digits")
        return digits
