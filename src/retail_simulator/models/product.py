
from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    category: str
    price: float
    product_name: str | None = None  # Extra field to store original unprocessed ID

    def __init__(self, **data):
        original_id = data.get("product_id", "")
        data["product_id"] = original_id.lower().strip()
        data["product_name"] = original_id
        super().__init__(**data)

    def __repr__(self):
        return (
            f"Product(product_id={self.product_id}, category={self.category}, price={self.price})"
        )
