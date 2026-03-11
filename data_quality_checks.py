from utils.logger import logger


def run_data_quality_checks(df, table_name):

    logger.info(f"Starting data quality checks for {table_name}")

    # Row count
    row_count = len(df)
    logger.info(f"{table_name} row count: {row_count}")

    # Null values
    null_counts = df.isnull().sum()

    for column, count in null_counts.items():

        if count > 0:
            logger.warning(f"{table_name}: {count} NULL values found in column {column}")

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        logger.warning(f"{table_name}: {duplicates} duplicate rows found")

    logger.info(f"Data quality checks completed for {table_name}")