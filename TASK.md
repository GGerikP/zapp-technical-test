
# Task overview

This task should take approximately 1-2 hours to complete. We are looking for high quality code instead of a rushed solution.
If you are running out of time, please provide a partial solution that is still high in quality
and explain what you would have done next. You will not be penalised for a partial solution that is written well.

Please write a README.md file with instructions on how to run the code and any additional information you think is relevant.

Your task is to create a simulation of a business with products sold in multiple stores and variable number of daily customers.
The simulation takes its initial parameters from a parameters.json file.
The programme must be able to adapt to changes in values in the parameters file, including the number of products, stores, and customers.

The Task is to create a simulation of a business with products sold in multiple stores and a variable number of daily customers.
The simulation parameters, such as the number of products, stores, and customers, should be configurable via the parameters.json file included in this folder

The program must be dynamic and able to adapt to any changes in the values provided in parameters.json, including but not limited to:
•   The number of products.
•	The number of stores.
•	The number of daily customers.


# Deliverables

1.	The complete Python code, organized and well-documented.
2.	Output files from running the code below
3.	Unit tests to verify key functionalities, such as (no need for 100% coverage):
    •	Proper handling of stockouts.
    •	Revenue calculations.


# Simulation Behaviour

The simulation should implement the following features:
1.	Daily Customer Activity:
    •	Each day, the number of customers defined by "number_of_customers_per_day" in parameters.json will visit stores.
    •	Customers randomly choose a store and purchase "units_ordered_per_day_per_customer" random products. These items can be identical or different.
2.	Stock Levels Management:
    •	Stock levels for each product at each store should initialize based on the "starting_stock_levels" field in parameters.json.
    •	At the end of each day, the stock levels should be updated:
        •	Subtracted based on sales.
        •	Restocked to the same "starting_stock_levels" at the start of the next day.
3.	Snapshots:
    •	When the generate_snapshot method is called the simulation should capture a snapshot of the business at the START of the current day
    •	Snapshots should be saved to files, named by the date (e.g., 2024-11-27.json).
4.	Handling Stockouts:
    •	If a product is out of stock, customers should choose another available product.
    •	If all products are out of stock, the customer should leave the store without purchasing anything.
5.	Simulation Length:
    •	It must support simulations running for at least 10 days.
6. Error Handling:
    •	Include safeguards to validate parameters.json to ensure it contains all necessary fields and valid values
        (e.g., positive integers for stock levels, non-negative customers).
7. Definition:
    • The simulation should be a class with the following methods:
