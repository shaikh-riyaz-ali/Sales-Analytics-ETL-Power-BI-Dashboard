from extract.extract_data import extract_data

from transform.clean_orders import clean_orders
from transform.clean_customers import clean_customers
from transform.clean_products import clean_products

from validation.schema_validator import validate_schema
from validation.data_quality_checks import run_data_quality_checks

from load.load_data import load_data

from utils.logger import logger


def run_pipeline():

    logger.info("Pipeline started")

    # -------------------------------------
    # Extract
    # -------------------------------------
    orders, customers, products = extract_data()

    # -------------------------------------
    # Transform
    # -------------------------------------
    orders_clean = clean_orders(orders)
    customers_clean = clean_customers(customers)
    products_clean = clean_products(products)

    # -------------------------------------
    # Schema Validation
    # -------------------------------------
    validate_schema(orders_clean, "orders")
    validate_schema(customers_clean, "customers")
    validate_schema(products_clean, "products")

    # -------------------------------------
    # Data Quality Checks
    # -------------------------------------
    run_data_quality_checks(orders_clean, "orders")
    run_data_quality_checks(customers_clean, "customers")
    run_data_quality_checks(products_clean, "products")

    # -------------------------------------
    # Load
    # -------------------------------------
    load_data(orders_clean, "orders_clean.csv")
    load_data(customers_clean, "customers_clean.csv")
    load_data(products_clean, "products_clean.csv")

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()