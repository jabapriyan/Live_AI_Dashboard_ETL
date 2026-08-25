from database import get_connection
from utils.logger import logger

from extract.traffic_scraper import (
    fetch_traffic_datas,
    fetch_data_month
)
from transform.clean import clean_traffic_data

from load.mysql_loader import (
    load_category,
    load_subscription,
    load_tools,
    load_statistics
)


logger.info("ETL process started")


# =========================================================
# DATABASE CONNECTION
# =========================================================

connection = get_connection()

if connection is None:

    logger.error("Database Connection Failed")

else:

    logger.info("Database Connection Successful")

    connection.close()

    logger.info("Database connection closed")


# =========================================================
# EXTRACT
# =========================================================

logger.info("Traffic scraping started")

url = "https://www.aicpb.com/en/ai-rankings/products/ai-chatbot-rankings/websites"

data = fetch_traffic_datas(url)
data_month = fetch_data_month(url)

print("Data Month:", data_month)

# =========================================================
# TRANSFORM + LOAD
# =========================================================

if data is not None:

    print("Page extracted successfully")

    print("Total records:", len(data))

    # TRANSFORM

    cleaned_data = clean_traffic_data(data)

    print("\nCleaned Data:")
    print(cleaned_data)

    # DIMENSION TABLES

    print("\nLoading Category...")

    load_category()

    print("Loading Subscription...")

    load_subscription()

    print("Loading Tools...")

    load_tools(cleaned_data)

    # FACT TABLE

    print("Loading Statistics...")

    load_statistics(cleaned_data,data_month)

    print("\nETL Load completed successfully")

else:

    print("Page extraction failed")
