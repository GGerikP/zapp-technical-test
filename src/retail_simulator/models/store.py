
import pandas as pd
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, PrivateAttr, model_validator

from retail_simulator.models.product import Product
from retail_simulator.models.sku import SKU


class Store(BaseModel):
    store_id: str = ""
    store_name: str
    store_location: str
    customer_count: int = Field(default=0)
    skus: Dict[str, SKU] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def post_init_setup(self) -> str:
        self.store_id = self.store_name.lower().strip()
        return self

    def add_skus(self, skus: List[SKU]) -> List[SKU]:
        new_skus = []
        for sku in skus:
            new_sku = self.add_sku(
                product=sku.product,
                starting_stock_levels=sku.get_starting_stock_levels(),
            )
            if new_sku is not None:
                new_skus.append(new_sku)
        return new_skus

    def add_sku(
        self,
        product: Product,
        starting_stock_levels: int
    ) -> Optional[SKU]:
        if product.product_id not in self.skus:
            new_sku = SKU(
                product=product,
                category=product.category,
                starting_stock_levels=starting_stock_levels,
                current_stock_levels=starting_stock_levels,
            )
            self.skus[product.product_id] = new_sku
            return new_sku
        return None

    def get_sku_by_product_id(
        self,
        product_id: str,
    ) -> Optional[SKU]:
        return self.skus.get(product_id)

    def get_skus(
        self
    ) -> List[SKU]:
        return list(self.skus.values())

    def restock_skus(
        self
    ) -> bool:
        for sku in self.get_skus():
            sku.reset_stock_to_starting_stock_levels()
        return True

    def get_skus_by_category(
        self,
        category: str,
    ) -> List[SKU]:
        skus_in_category = [
            sku for sku in self.skus.values() if sku.category == category
        ]
        return skus_in_category

    def __repr__(self):
        return f"Store({self.store_id}, {self.store_name}, {self.store_location})"
