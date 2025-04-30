import json
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class ProductJSONConfig(BaseModel):
    product: str
    category: str
    price: int = Field(..., ge=0)

class SKUJSONConfig(BaseModel):
    product: str
    starting_stock_levels: int = Field(..., ge=0)

class StoreJSONConfig(BaseModel):
    name: str
    location: str
    products: List[SKUJSONConfig]

class CustomerJSONConfig(BaseModel):
    units_ordered_per_day_per_customer: int = Field(..., ge=0)
    number_of_customers_per_day: int = Field(..., ge=0)

class ConfigJSON(BaseModel):
    start_date: date
    products: List[ProductJSONConfig]
    stores: List[StoreJSONConfig]
    customers: CustomerJSONConfig

class Config:

    def __init__(self, parameters_file_path: str) -> None:
        """Initialize the Config class with the path to the parameters file"""
        if not parameters_file_path:
            raise ValueError("The parameters file path cannot be empty.")
        self.__initialize_system_configuration(parameters = self.__parse_parameters_file(parameters_file_path))

    def __parse_parameters_file(self, parameters_file_path: str) -> ConfigJSON:
        """Parse the parameters file and return the parameters as a dictionary"""
        with open(parameters_file_path, 'r') as file:
            parameters = json.load(file)
        validated_config = ConfigJSON.model_validate(parameters)
        return validated_config

    def __initialize_system_configuration(self, parameters: ConfigJSON) -> None:
        """Initialize the system configuration with the parameters"""
        self.start_date = parameters.start_date
        self.products = parameters.products
        self.stores = parameters.stores
        self.customers = parameters.customers
