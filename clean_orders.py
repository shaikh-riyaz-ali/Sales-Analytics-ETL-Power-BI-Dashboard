import pandas as pd
from utils.config_loader import load_config
from utils.logger import logger

rules = load_config("config/business_rules.yaml")


def clean_orders(df):

    logger.info("Starting orders cleaning")

    order_rules = rules["orders"]

    # ----------------------------------------
    # Step 1: Clean column names
    # ----------------------------------------
    df.columns = df.columns.str.strip()
    logger.info("Column names whitespace removed")

    # ----------------------------------------
    # Step 2: Column mapping
    # ----------------------------------------
    column_mapping = order_rules.get("column_mapping", {})
    df = df.rename(columns=column_mapping)

    logger.info("Column mapping applied")

    # ----------------------------------------
    # Step 3: Strip whitespace from string columns
    # ----------------------------------------
    if "payment_method" in df.columns:

        df["payment_method"] = df["payment_method"].astype(str).str.strip().str.lower()

        logger.info("Whitespace cleaned in payment_method")

    # ----------------------------------------
    # Step 4: Datatype conversion (from YAML)
    # ----------------------------------------
    datatype_rules = order_rules.get("datatype_conversion", {})

    for column, dtype in datatype_rules.items():

        if column in df.columns:

            try:

                if dtype == "datetime":
                    df[column] = pd.to_datetime(df[column], errors="coerce")

                elif dtype in ["int", "float"]:
                    df[column] = pd.to_numeric(df[column], errors="coerce")

                elif dtype == "string":
                    df[column] = df[column].astype(str)

                logger.info(f"{column} converted to {dtype}")

            except Exception as e:

                logger.error(f"Datatype conversion failed for {column}: {str(e)}")

    # ----------------------------------------
    # Step 5: Remove negative values
    # ----------------------------------------
    if "remove_negative_values" in order_rules:

        for col in order_rules["remove_negative_values"]:

            if col in df.columns:

                before = len(df)

                df = df[df[col] >= 0]

                after = len(df)

                logger.info(f"Removed {before-after} rows with negative {col}")

    # ----------------------------------------
    # Step 6: Remove duplicates
    # ----------------------------------------
    if "remove_duplicates" in order_rules:

        subset = order_rules["remove_duplicates"]["subset"]

        before = len(df)

        df = df.drop_duplicates(subset=subset)

        after = len(df)

        logger.info(f"Duplicates removed: {before-after}")

    # ----------------------------------------
    # Step 7: Drop rows with critical null values
    # ----------------------------------------
    critical_columns = ["order_id", "customer_id", "product_id", "order_date"]

    before = len(df)

    df = df.dropna(subset=[col for col in critical_columns if col in df.columns])

    after = len(df)

    logger.info(f"Rows removed due to null critical fields: {before-after}")

    logger.info("Orders cleaning completed")

    return df