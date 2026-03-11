import pandas as pd
from utils.config_loader import load_config
from utils.logger import logger

rules = load_config("config/business_rules.yaml")


def clean_products(df):

    logger.info("Starting products cleaning")

    product_rules = rules["products"]

    # ------------------------------------------------
    # Step 1: Clean column names
    # ------------------------------------------------
    df.columns = df.columns.str.strip()
    logger.info("Column names whitespace removed")

    # ------------------------------------------------
    # Step 2: Column mapping
    # ------------------------------------------------
    column_mapping = product_rules.get("column_mapping", {})
    df = df.rename(columns=column_mapping)

    logger.info("Column mapping applied")

    # ------------------------------------------------
    # Step 3: Strip whitespace from string columns
    # ------------------------------------------------
    for col in ["product_name", "category", "brand"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    logger.info("Whitespace removed from product text fields")

    # ------------------------------------------------
    # Step 4: Datatype conversion (from YAML)
    # ------------------------------------------------
    datatype_rules = product_rules.get("datatype_conversion", {})

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

    # ------------------------------------------------
    # Step 5: Category mapping
    # ------------------------------------------------
    if "category_mapping" in product_rules and "category" in df.columns:

        df["category"] = df["category"].replace(product_rules["category_mapping"])

        logger.info("Category mapping applied")

    # ------------------------------------------------
    # Step 6: Brand mapping
    # ------------------------------------------------
    if "brand_mapping" in product_rules and "brand" in df.columns:

        df["brand"] = df["brand"].replace(product_rules["brand_mapping"])

        logger.info("Brand mapping applied")

    # ------------------------------------------------
    # Step 7: Remove duplicates
    # ------------------------------------------------
    if "remove_duplicates" in product_rules:

        subset = product_rules["remove_duplicates"]["subset"]

        before = len(df)

        df = df.drop_duplicates(subset=subset)

        after = len(df)

        logger.info(f"Duplicates removed: {before-after}")

    logger.info("Products cleaning completed")

    return df