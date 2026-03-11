import pandas as pd
from utils.logger import logger

def extract_data():

    logger.info("Starting data extraction")

    orders = pd.read_csv(r"C:\Users\riyaz\OneDrive\Desktop\resume_project\data\raw\orders.csv")
    customers = pd.read_csv(r"C:\Users\riyaz\OneDrive\Desktop\resume_project\data\raw\customers.csv")
    products = pd.read_csv(r"C:\Users\riyaz\OneDrive\Desktop\resume_project\data\raw\products.csv")

    logger.info("Data extraction completed")

    return orders, customers, products