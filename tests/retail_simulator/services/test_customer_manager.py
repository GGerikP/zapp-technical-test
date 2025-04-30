import pytest
from retail_simulator.services.customer_manager import CustomerManager
from retail_simulator.config.config import CustomerJSONConfig
from retail_simulator.models.customer import Customer

@pytest.fixture
def customer_config():
    return CustomerJSONConfig(
        units_ordered_per_day_per_customer=5,
        number_of_customers_per_day=3
    )


@pytest.fixture
def customer_manager(customer_config):
    return CustomerManager(customer_config=customer_config)


def test_customer_manager_initialization(customer_manager, customer_config):
    assert customer_manager.daily_purchase_count == customer_config.units_ordered_per_day_per_customer
    assert len(customer_manager.customers) == customer_config.number_of_customers_per_day


def test_add_customers(customer_manager, customer_config):
    initial_customer_count = len(customer_manager.customers)
    new_customers = customer_manager.add_customers(customer_config)
    assert len(new_customers) == customer_config.number_of_customers_per_day
    assert len(customer_manager.customers) == initial_customer_count + customer_config.number_of_customers_per_day


def test_add_customer(customer_manager):
    initial_customer_count = len(customer_manager.customers)
    new_customer = customer_manager.add_customer(daily_purchase_count=5)
    assert new_customer.customer_id == initial_customer_count + 1
    assert new_customer.number_of_purchases_left_to_make == 5
    assert len(customer_manager.customers) == initial_customer_count + 1


def test_reset_customer_units_to_buy(customer_manager):
    for customer in customer_manager.customers.values():
        customer.number_of_purchases_left_to_make = 0
    customer_manager.reset_customer_units_to_buy()
    for customer in customer_manager.customers.values():
        assert customer.number_of_purchases_left_to_make == customer_manager.daily_purchase_count