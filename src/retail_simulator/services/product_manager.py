import pandas as pd
from typing import List, Optional

from retail_simulator.config.config import ProductJSONConfig
from retail_simulator.models.product import Product


class ProductManager:

    products: pd.DataFrame

    def __init__(
            self,
            products: List[Product] = None,
            products_config: List[ProductJSONConfig] = None
    ) -> None:
        columns = list(Product.model_fields.keys())
        if products is None or len(products) == 0:
            self.products = pd.DataFrame({col: pd.Series(dtype="object") for col in columns})
        else:
            self.products = pd.DataFrame([p.model_dump() for p in products])

        if products_config is not None:
            self.add_products(products_config)

    def add_product(
            self,
            product_id: str,
            category: str,
            price: int
    ) -> Optional[Product]:
        if not product_id in self.products['product_id'].values:
            new_product = Product(
                product_id=product_id,
                category=category,
                price=price
            )
            new_row = pd.DataFrame([new_product.model_dump()], columns=self.products.columns)
            new_row = new_row.astype(self.products.dtypes.to_dict())
            self.products = pd.concat([self.products, new_row], ignore_index=True)

            return new_product
        return None

    def add_products(self, products_config: List[ProductJSONConfig]) -> List[Product]:
        new_products = []
        for product in products_config:
            product: ProductJSONConfig
            new_product = self.add_product(
                    product_id=product.product,
                    category=product.category,
                    price=product.price
                )
            if new_product is not None:
                new_products.append(new_product)
        return new_products

    def remove_product(self, product_id: str) -> None:
        if product_id not in self.products['product_id'].values:
            raise ValueError("Product ID does not exist.")
        self.products = self.products[self.products['product_id'] != product_id]

    def update_product(self, product_id: str, category: str = None, price: int = None) -> None:
        if product_id not in self.products['product_id'].values:
            raise ValueError("Product ID does not exist.")
        if category is not None:
            self.products.loc[self.products['product_id'] == product_id, 'category'] = category
        if price is not None:
            self.products.loc[self.products['product_id'] == product_id, 'price'] = price

    def get_product(self, product_id: str) -> Product:
        product_row = self.products[self.products['product_id'] == product_id.lower().strip()]
        if product_row.empty:
            return None
        return Product(**product_row.iloc[0])

