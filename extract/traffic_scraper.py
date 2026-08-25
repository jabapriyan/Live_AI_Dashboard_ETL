import requests
from bs4 import BeautifulSoup
from utils.logger import logger
import time


def fetch_traffic_datas(url):

    for attempt in range(3):

        try:
            response = requests.get(
                url,
                timeout=30,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            print("Status Code:", response.status_code)

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            print("HTML Length:", len(response.text))
            print("ChatGPT found:", "ChatGPT" in response.text)

            # Find all ranking rows
            rows = soup.select("div.group.grid")

            print("Number of ranking rows:", len(rows))

            # Store all extracted records
            all_data = []

            for row in rows:

                values = row.get_text(" ", strip=True)

                parts = values.split()

                rank = parts[0]

                visits = parts[-2]

                mom = parts[-1]

                tool = " ".join(parts[1:-2])

                data = {
                    "Rank": rank,
                    "Tool": tool,
                    "Monthly_Visits": visits,
                    "MoM": mom
                }

                all_data.append(data)

            logger.info(
                f"Traffic data extracted successfully: {len(all_data)} records"
            )

            return all_data

        except requests.exceptions.RequestException as e:

            print(f"Attempt {attempt + 1} failed:", e)

            logger.error(
                f"Traffic extraction failed: {e}"
            )

            if attempt < 2:
                time.sleep(2)

    return None


def fetch_data_month(url):

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        page_text = soup.get_text(" ", strip=True)

        import re

        match = re.search(
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})\s+Edition',
            page_text
        )

        if match:

            month = match.group(1)
            year = match.group(2)

            month_numbers = {
                "Jan": "01",
                "Feb": "02",
                "Mar": "03",
                "Apr": "04",
                "May": "05",
                "Jun": "06",
                "Jul": "07",
                "Aug": "08",
                "Sep": "09",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12"
            }

            month_number = month_numbers[month]

            data_month = f"{year}-{month_number}-01"

            logger.info(
                f"Data month extracted successfully: {data_month}"
            )

            return data_month

        logger.error("Data month not found")

        return None

    except requests.exceptions.RequestException as e:

        logger.error(
            f"Data month extraction failed: {e}"
        )

        return None