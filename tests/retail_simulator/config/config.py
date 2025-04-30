import pytest
import json
from retail_simulator.config.config import Config, ConfigJSON, CustomerJSONConfig, ProductJSONConfig, StoreJSONConfig, SKUJSONConfig
from datetime import date
from unittest.mock import mock_open, patch

@pytest.fixture
def valid_config_data():
    return {
        "start_date": "2025-01-01",
        "products": [
            {"product": "Laptop", "category": "Electronics", "price": 1000},
            {"product": "Phone", "category": "Electronics", "price": 500}
        ],
        "stores": [
            {
                "name": "Store A",
                "location": "City A",
                "products": [
                    {"product": "Laptop", "starting_stock_levels": 10},
                    {"product": "Phone", "starting_stock_levels": 20}
                ]
            }
        ],
        "customers": {
            "units_ordered_per_day_per_customer": 5,
            "number_of_customers_per_day": 3
        }
    }


def test_parse_parameters_file_valid(valid_config_data):
    mock_file_content = json.dumps(valid_config_data)
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        config = Config(parameters_file_path="dummy_path")
        assert config.start_date == date(2025, 1, 1)
        assert len(config.products) == 2
        assert config.products[0].product == "Laptop"
        assert config.products[1].price == 500
        assert len(config.stores) == 1
        assert config.stores[0].name == "Store A"
        assert config.customers.units_ordered_per_day_per_customer == 5


def test_parse_parameters_file_invalid_json():
    invalid_json_content = "{invalid_json}"
    with patch("builtins.open", mock_open(read_data=invalid_json_content)):
        with pytest.raises(json.JSONDecodeError):
            Config(parameters_file_path="dummy_path")


def test_parse_parameters_file_missing_fields():
    incomplete_data = {
        "start_date": "2025-01-01",
        "products": []
    }
    mock_file_content = json.dumps(incomplete_data)
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with pytest.raises(ValueError):
            Config(parameters_file_path="dummy_path")