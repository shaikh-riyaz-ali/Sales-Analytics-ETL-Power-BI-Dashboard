import pandas as pd
from utils.config_loader import load_config
from utils.logger import logger


def validate_schema(df, table_name):

    logger.info(f"Starting schema validation for {table_name}")

    # Load schema config
    schema_config = load_config("config/schema.yaml")

    if table_name not in schema_config:
        logger.error(f"No schema defined for table: {table_name}")
        raise ValueError(f"Schema not found for {table_name}")

    table_schema = schema_config[table_name]["columns"]

    # ------------------------------------------------
    # Step 1: Check required columns
    # ------------------------------------------------
    expected_columns = list(table_schema.keys())
    actual_columns = df.columns.tolist()

    missing_columns = [col for col in expected_columns if col not in actual_columns]

    if missing_columns:
        logger.error(f"{table_name} missing columns: {missing_columns}")
        raise ValueError(f"{table_name} schema validation failed")

    logger.info(f"All required columns present for {table_name}")

    # ------------------------------------------------
    # Step 2: Datatype validation
    # ------------------------------------------------
    for column, expected_type in table_schema.items():

        if column not in df.columns:
            continue

        actual_dtype = str(df[column].dtype)

        try:

            if expected_type == "int":

                if not pd.api.types.is_integer_dtype(df[column]):
                    logger.warning(
                        f"{table_name}.{column} expected int but got {actual_dtype}"
                    )

            elif expected_type == "float":

                if not pd.api.types.is_float_dtype(df[column]):
                    logger.warning(
                        f"{table_name}.{column} expected float but got {actual_dtype}"
                    )

            elif expected_type == "string":

                if not pd.api.types.is_object_dtype(df[column]):
                    logger.warning(
                        f"{table_name}.{column} expected string but got {actual_dtype}"
                    )

            elif expected_type == "datetime":

                if not pd.api.types.is_datetime64_any_dtype(df[column]):
                    logger.warning(
                        f"{table_name}.{column} expected datetime but got {actual_dtype}"
                    )

        except Exception as e:

            logger.error(f"Error validating column {column}: {str(e)}")

    logger.info(f"Schema validation completed for {table_name}")