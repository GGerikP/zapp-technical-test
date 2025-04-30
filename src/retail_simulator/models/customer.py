
from datetime import date
import random
from typing import List
from pydantic import BaseModel, Field

from retail_simulator.models.sku import SKU
from retail_simulator.models.store import Store



class Customer(BaseModel):

    # It would be better to use UUIDs, but for simplicity we're using ints
    customer_id: int
    number_of_purchases_left_to_make: int = Field(..., ge=0)

    model_config = {"arbitrary_types_allowed": True}

    def make_purchases(
        self,
        store: Store,
        date: date,
    ) -> None:
        while self.number_of_purchases_left_to_make > 0:
            sku = random.choice(store.get_skus())
            self.make_purchase(
                store=store,
                sku=sku,
                amount=random.randint(1, 5),
                price=sku.product.price,
                date=date,
            )

    def make_purchase(
        self,
        store: Store,
        sku: SKU,
        amount: int,
        price: int,
        date: date,
        skus_in_category: List[SKU] = None,
    ) -> None:
        if self.number_of_purchases_left_to_make <= 0:
            raise ValueError("No purchases left to make.")

        amount = min(self.number_of_purchases_left_to_make, amount)

        sku = store.get_sku_by_product_id(sku.product.product_id)

        # Attempt to pull the stock from the SKU - if it fails, try another SKU from the same category
        if sku is None or not sku.adjust_current_stock_amount(amount):
            self.purchase_another_sku_within_category(
                store=store,
                sku=sku,
                amount=amount,
                price=price,
                date=date,
                skus_in_category=skus_in_category,
            )

        self.number_of_purchases_left_to_make -= amount

    def purchase_another_sku_within_category(
        self,
        store: Store,
        sku: SKU,
        amount: int,
        price: int,
        date: date,
        skus_in_category: List[SKU] = None,
    ) -> None:
        if skus_in_category is None:
            skus_in_category = store.get_skus_by_category(sku.category)

        # Don't try the current SKU again
        if sku is not None and sku in skus_in_category:
            skus_in_category = [s for s in skus_in_category if s != sku]

        if len(skus_in_category) > 0:
            sku = random.choice(skus_in_category)
            skus_in_category = [s for s in skus_in_category if s != sku]

            return self.make_purchase(
                store=store,
                sku=sku,
                amount=amount,
                price=price,
                date=date,
                skus_in_category=skus_in_category
            )


