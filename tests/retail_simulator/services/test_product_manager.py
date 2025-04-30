import pytest
import pandas as pd
from retail_simulator.services.product_manager import ProductManager
from retail_simulator.models.product import Product
from retail_simulator.config.config import ProductJSONConfig

@pytest.fixture
def sample_products():
    return [
        Product(product_id="laptop", category="electronics", price=1000),
        Product(product_id="phone", category="electronics", price=500)
    ]


@pytest.fixture
def sample_products_config():
    return [
        ProductJSONConfig(product="tablet", category="electronics", price=300),
        ProductJSONConfig(product="monitor", category="electronics", price=200)
    ]


@pytest.fixture
def product_manager(sample_products):
    return ProductManager(products=sample_products)


def test_initialization_with_products(sample_products):
    manager = ProductManager(products=sample_products)
    assert len(manager.products) == 2
    assert "laptop" in manager.products["product_id"].values


def test_initialization_with_empty_products():
    manager = ProductManager()
    assert manager.products.empty


def test_add_product(product_manager):
    new_product = product_manager.add_product(product_id="tablet", category="electronics", price=300)
    assert new_product is not None
    assert new_product.product_id == "tablet"
    assert len(product_manager.products) == 3


def test_add_existing_product(product_manager):
    new_product = product_manager.add_product(product_id="laptop", category="electronics", price=1200)
    assert new_product is None
    assert len(product_manager.products) == 2


def test_add_products(product_manager, sample_products_config):
    new_products = product_manager.add_products(sample_products_config)
    assert len(new_products) == 2
    assert len(product_manager.products) == 4


def test_remove_product(product_manager):
    product_manager.remove_product("laptop")
    assert len(product_manager.products) == 1
    assert "laptop" not in product_manager.products["product_id"].values


def test_remove_nonexistent_product(product_manager):
    with pytest.raises(ValueError):
        product_manager.remove_product("nonexistent")


def test_update_product(product_manager):
    product_manager.update_product(product_id="laptop", category="computers", price=1200)
    updated_product = product_manager.products[product_manager.products["product_id"] == "laptop"].iloc[0]
    assert updated_product["category"] == "computers"
    assert updated_product["price"] == 1200


def test_update_nonexistent_product(product_manager):
    with pytest.raises(ValueError):
        product_manager.update_product(product_id="nonexistent", category="computers")


def test_get_product(product_manager):
    product = product_manager.get_product("laptop")
    assert product is not None
    assert product.product_id == "laptop"


def test_get_nonexistent_product(product_manager):
    product = product_manager.get_product("nonexistent")
    assert product is None