from pydantic import BaseModel, Field, field_validator


class OrderCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=1, le=100)

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "product_name не может быть пустым или состоять из пробелов"
            )
        return v


class OrderResponse(OrderCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
