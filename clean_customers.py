import pandas as pd
from utils.config_loader import load_config
from utils.logger import logger

rules = load_config("config/business_rules.yaml")


def clean_customers(df):

    logger.info("Starting customers cleaning")

    customer_rules = rules["customers"]

    # ------------------------------------------------
    # Step 1: Clean column names
    # ------------------------------------------------
    df.columns = df.columns.str.strip()
    logger.info("Column names cleaned")

    # ------------------------------------------------
    # Step 2: Rename columns using mapping
    # ------------------------------------------------
    column_mapping = customer_rules["column_mapping"]
    df = df.rename(columns=column_mapping)

    logger.info("Column mapping applied")

    # ------------------------------------------------
    # Step 3: Clean values (strip spaces)
    # ------------------------------------------------
    df["city"] = df["city"].astype(str).str.strip()
    df["state"] = df["state"].astype(str).str.strip()

    logger.info("Whitespace removed from city/state")

# ------------------------------------------------
    # Step 4: Fill missing values using YAML rules
    # ------------------------------------------------
    if "fillna" in customer_rules:

        for column, value in customer_rules["fillna"].items():

            if column in df.columns:

                missing_before = df[column].isna().sum()

                df[column] = df[column].fillna(value)

                logger.info(f"{missing_before} missing values filled in {column} with '{value}'")

    # ------------------------------------------------
    # Step 5: Apply city mapping
    # ------------------------------------------------
    if "city_mapping" in customer_rules:

        df["city"] = df["city"].replace(customer_rules["city_mapping"])

        logger.info("City mapping applied")

    # ------------------------------------------------
    # Step 6: Apply state mapping
    # ------------------------------------------------
    if "state_mapping" in customer_rules:

        df["state"] = df["state"].replace(customer_rules["state_mapping"])

        logger.info("State mapping applied")

    # ------------------------------------------------
    # Step 7: Remove duplicates
    # ------------------------------------------------
    if "remove_duplicates" in customer_rules:

        subset = customer_rules["remove_duplicates"]["subset"]

        before = len(df)

        df = df.drop_duplicates(subset=subset)

        after = len(df)

        logger.info(f"Duplicates removed: {before - after}")

    logger.info("Customers cleaning completed")

    return df