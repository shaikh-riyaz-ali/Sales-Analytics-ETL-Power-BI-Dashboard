# Sales Data Analytics ETL Pipeline

## Project Overview
This project demonstrates an end-to-end data analytics workflow including data extraction, transformation, validation, and reporting.

The pipeline processes large-scale sales datasets and prepares analytics-ready data for Power BI dashboards.

## Technologies Used
- Python
- Pandas
- YAML
- ETL Pipeline
- Power BI
- DAX

## Project Architecture

Raw Data → Data Cleaning → Schema Validation → Data Quality Checks → Processed Data → Power BI Dashboard

## Key Features

- Config-driven ETL pipeline using YAML
- Automated data cleaning with Pandas
- Schema validation framework
- Data quality monitoring
- Logging system for pipeline tracking
- Power BI dashboard with advanced DAX measures

## Dataset

The pipeline processes three datasets:

- Orders
- Customers
- Products

Total processed records: **1M+ rows**

## Power BI Dashboard

The dashboard contains 3 pages:

1. Sales Performance
2. Customer Insights
3. Product Analysis

Includes advanced DAX measures:

- YTD Sales
- MTD Sales
- YoY Growth
- Rolling 12 Month Sales

## How to Run the Pipeline

```bash
python pipeline/run_pipeline.py
