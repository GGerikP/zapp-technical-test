from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import json
import random
import traceback
from typing import List
from retail_simulator.config.config import Config
from retail_simulator.models.customer import Customer
from retail_simulator.models.sku import SKU
from retail_simulator.models.store import Store
from retail_simulator.services.customer_manager import CustomerManager
from retail_simulator.services.product_manager import ProductManager
from retail_simulator.services.store_manager import StoreManager

class Simulation:

    def __init__(self, parameters_file_path: str):
        """Read the parameters from the parameters.json file and initialize the simulation with the correct parameters"""

        if not parameters_file_path:
            raise ValueError("The parameters file path cannot be empty.")
        self.config = Config(parameters_file_path)
        self.date = self.config.start_date
        self.product_manager = ProductManager(products_config=self.config.products)
        self.store_manager = StoreManager(product_manager=self.product_manager, store_list_config=self.config.stores)
        self.customer_manager = CustomerManager(customer_config=self.config.customers)

    def run(self, days: int):
        """Run the simulation for the specified number of days. For each day the method should first simulate the orders,
        create a snapshot of the day using self._generate_snapshot() and then fully restock the stores at the end of each day.
        """
        print('***********************************************************************************************************')
        print(f'Running simulation for {days} days')
        for i in range(days):
            print(f'Day {i}')
            self._generate_snapshot()
            self.customer_manager.reset_customer_units_to_buy()
            self._restock_stores()
            self._simulate_orders()
            self.date += timedelta(days=1)

    def _simulate_orders(
        self
    ) -> None:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for customer in self.customer_manager.customers.values():
                customer: Customer
                store = random.choice(list(self.store_manager.stores.values()))
                store.customer_count += 1
                executor.submit(self._make_purchases, customer, store)

    def _make_purchases(
        self,
        customer: Customer,
        store: Store
    ) -> None:
        try:
            customer.make_purchases(
                store=store,
                date=self.date,
            )
        except (Exception, ValueError) as e:
            print(f'Error making purchase: {e}')
            print(traceback.format_exc())
            return []

    def _restock_stores(
            self
    ) -> None:
        self.store_manager.restock_stores()

    def _generate_snapshot(
        self,
    ) -> None:
        """Create a file which captures the snapshot of the business, named by the date (e.g., 2024-11-27.json).
        The file should include the current stock levels for all products and stores and the orders made by each customer during the day.
        """
        print('Generating snapshot of the business')

        data = {}
        for store in self.store_manager.stores.values():
             store: Store
             skus = store.get_skus()
             data[store.store_id] = {
                "store_name": store.store_name,
                "store_location": store.store_location,
                "customer_count": store.customer_count,
                "skus": [sku.to_sales_snapshot_dict() for sku in store.get_skus()],
             }
        with open(self.date.strftime("%Y-%m-%d") + ".json", 'w') as file:
                json.dump(data, file, indent=2)
        print(f'Snapshot saved to {self.date}.json')

