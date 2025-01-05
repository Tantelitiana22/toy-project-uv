from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    price: float
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "pizza",
                "price": 3.14,
                "description": "Italian food"
            }
        }


class Product(ProductBase, table=True):
    id: int = Field(primary_key=True, default=None)


class ProductInput(ProductBase):
    pass

class ProductOutput(ProductBase):
    id: int
