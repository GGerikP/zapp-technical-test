from threading import Lock

from pydantic import BaseModel, PrivateAttr

from retail_simulator.models.product import Product

class SKU(BaseModel):
    product: Product

    # This structure is not ideal as we're duplicating the data
    # Normally this would be taken care of by a database relationship between the investory item and the product
    category: str
    starting_stock_levels: int
    current_stock_levels: int

    # Add a thread lock
    _lock: Lock = PrivateAttr(default_factory=Lock)

    def get_starting_stock_levels(self) -> int:
        with self._lock:
            return self.starting_stock_levels

    def get_current_approximate_stock_levels(self) -> int:
        return self.current_stock_levels

    def adjust_current_stock_amount(self, quantity: int) -> bool:
        with self._lock:
            new_stock = self.current_stock_levels - quantity

            if new_stock < 0:
                return False  # Not enough stock

            self.current_stock_levels = new_stock
            return True
        return False

    def get_how_many_items_sold(self) -> int:
        return self.starting_stock_levels - self.current_stock_levels

    def reset_stock_to_starting_stock_levels(self) -> None:
        with self._lock:
            self.current_stock_levels = self.starting_stock_levels

    def revenue(self) -> float:
        return self.get_how_many_items_sold() * self.product.price

    def to_sales_snapshot_dict(self) -> dict:
        with self._lock:
            return {
                "product": self.product.product_id,
                "category": self.category,
                "current_stock_levels": self.current_stock_levels,
                "stock_sold": self.get_how_many_items_sold(),
                "revenue": self.revenue(),
            }

    def __str__(self) -> str:
        return (
            f"SKU(product={self.product}, category={self.category}, "
            f"starting_stock_levels={self.starting_stock_levels}, "
            f"current_stock_levels={self.current_stock_levels})"
        )

