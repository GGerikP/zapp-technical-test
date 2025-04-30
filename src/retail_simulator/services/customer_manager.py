
from typing import Dict, List
import pandas as pd
from retail_simulator.config.config import CustomerJSONConfig
from retail_simulator.models.customer import Customer
from retail_simulator.models.store import Store


class CustomerManager:

    customers: Dict[int, Store] = {}
    daily_purchase_count: int = 0

    def __init__(
        self,
        customer_config: CustomerJSONConfig = None
    ):
        if customer_config is not None:
            self.daily_purchase_count = customer_config.units_ordered_per_day_per_customer
            self.add_customers(customer_config)

    def add_customers(self, customer_config: CustomerJSONConfig) -> List[Customer]:
        new_customers = []
        for i in range(customer_config.number_of_customers_per_day):
            new_customers.append(self.add_customer(
                daily_purchase_count=self.daily_purchase_count
            ))
        return new_customers

    def add_customer(self, daily_purchase_count: int) -> Customer:
        customer_id = len(self.customers.keys()) + 1
        new_customer = Customer(
            customer_id=customer_id,
            number_of_purchases_left_to_make=daily_purchase_count,
        )
        self.customers[customer_id] = new_customer
        return new_customer

    def reset_customer_units_to_buy(self) -> bool:
        for customer in self.customers.values():
            customer: Customer
            customer.number_of_purchases_left_to_make = self.daily_purchase_count
        return True