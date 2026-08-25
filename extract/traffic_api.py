import requests
from utils.logger import logger

def fetch_traffic_data(url):
    try:
        response=requests.get(url,timeout=30)
        response.raise_for_status()

        data=response.json()

        logger.info("Trafic data extracted successfully")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Traffic API extraction failed {e}")

        return None