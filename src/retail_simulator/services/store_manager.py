from typing import Dict, List, Optional

from retail_simulator.config.config import SKUJSONConfig, StoreJSONConfig
from retail_simulator.models.sku import SKU
from retail_simulator.models.store import Store
from retail_simulator.services.product_manager import ProductManager

class StoreManager:

    stores: Dict[str, Store]

    def __init__(
        self,
        product_manager: ProductManager,
        store_list: Optional[List[Store]] = None,
        store_list_config: Optional[List[StoreJSONConfig]] = None,
    ) -> None:
        self.stores = {}
        self.product_manager = product_manager

        if store_list is not None:
            for store in store_list:
                self.stores[store.store_name] = store

        if store_list_config is not None:
            self.add_stores(store_list_config)

    def add_stores(self, store_list_config: List[StoreJSONConfig]) -> List[Store]:
        new_stores = []
        for store_config in store_list_config:
            new_store = self.add_store(
                store_name=store_config.name,
                store_location=store_config.location,
                sku_configs=store_config.products,
            )
            if new_store is not None:
                new_stores.append(new_store)
        return new_stores

    def add_store(
        self,
        store_name: str,
        store_location: str,
        sku_configs: List[SKUJSONConfig],
    ) -> Optional[Store]:
        if store_name not in self.stores:
            skus = []
            for sku_config in sku_configs:
                product = self.product_manager.get_product(
                    product_id=sku_config.product.lower().strip(),  # <- fix your call here
                )
                if product is not None:
                    skus.append(
                        SKU(
                            product=product,
                            category=product.category,
                            starting_stock_levels=sku_config.starting_stock_levels,
                            current_stock_levels=sku_config.starting_stock_levels,
                        )
                    )
            new_store = Store(
                store_name=store_name,
                store_location=store_location,
            )
            new_store.add_skus(skus)
            self.stores[store_name] = new_store
            return new_store
        return None

    def restock_stores(self) -> bool:
        for store in self.stores.values():
            store.restock_skus()
        return True