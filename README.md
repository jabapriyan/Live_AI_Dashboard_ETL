# AI Tools Traffic & Price Analysis Dashboard 📊

An end-to-end ETL (Extract, Transform, Load) pipeline that tracks **traffic and pricing trends across AI tools**, and visualizes them in a live, real-time Power BI dashboard.

---

## 🚀 Project Overview

This project automates the process of collecting, cleaning, and analyzing data on various AI tools — including their website traffic and pricing information — so trends can be monitored over time without manual data collection.

**Pipeline flow:**

```
Web Scraping + API  →  Data Cleaning/Transformation  →  MySQL Database  →  Power BI (Live Dashboard)
   (Extract)               (Transform)                     (Load)            (Visualize)
```

---

## 🛠️ Tech Stack

- **Python** — core ETL scripting
- **Web Scraping** — collecting AI tool traffic data from source websites
- **API Integration** — pulling supplementary pricing/tool data
- **MySQL** — relational database for storing cleaned, structured data
- **Power BI** — live dashboard connected directly to MySQL for real-time visualization
- **Python `schedule`/timer-based automation** — pipeline runs extraction at set intervals to keep data fresh

---

## ⚙️ How It Works

1. **Extract**
   - Scrapes AI tool traffic data from target websites (`traffic_scraper.py`)
   - Pulls traffic data via API (`traffic_api.py`)
   - Pulls AI tool metadata via the GitHub API (`github_api.py`, `metadata.py`)
   - Runs automatically on a timed schedule using Python

2. **Transform**
   - Cleans and structures raw scraped/API data
   - Handles missing values, formatting, and deduplication
   - Prepares data for relational storage

3. **Load**
   - Inserts the cleaned data into a **MySQL** database
   - Structured tables allow historical tracking of traffic and price changes over time

4. **Visualize**
   - **Power BI** connects live to the MySQL database
   - Dashboard updates in real-time as new data is loaded
   - Enables trend analysis on traffic and pricing across multiple AI tools

---

## 📁 Project Structure

```
Live_AI_Dashboard_ETL/
│
├── extract/
│   ├── github_api.py       # Pulls AI tool data via GitHub API
│   ├── traffic_api.py      # Pulls traffic data via API
│   ├── traffic_scraper.py  # Web scraping for traffic data
│   ├── metadata.py         # Extracts tool metadata
│   └── logs/
│
├── transform/
│   ├── clean.py             # Cleans and structures raw data
│   └── merge.py              # Merges data from multiple sources
│
├── load/
│   ├── mysql_loader.py      # Loads cleaned data into MySQL
│   │                          (load_category, load_subscription,
│   │                           load_tools, load_statistics)
│   └── logs/
│
├── utils/                    # Shared helper functions
├── logs/
│   └── etl.log                # Pipeline run logs
│
├── config.py                  # DB credentials (excluded via .gitignore)
├── database.py                # Database connection handler
├── main.py                    # Pipeline entry point
├── tools_config.py            # AI tools tracked by the pipeline
├── requirements.txt
└── README.md
```

> ⚠️ **Note:** `config.py` contains real database credentials and is excluded from this repository via `.gitignore`. To run this project yourself, create your own `config.py` with your MySQL connection details (`HOST`, `USER`, `DATABASE`, `PASSWORD`).

---

## ▶️ Running the Project

1. Clone the repository
   ```
   git clone https://github.com/jabapriyan/Live_AI_Dashboard_ETL.git
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Create your own `config.py` with your MySQL credentials:
   ```python
   HOST = "your_host"
   USER = "your_username"
   DATABASE = "your_database"
   PASSWORD = "your_password"
   ```

4. Run the pipeline
   ```
   python main.py
   ```

5. Connect Power BI to your MySQL database to view the live dashboard

---

## 📈 Future Improvements

- Add more AI tools/sources for broader market coverage
- Deploy scheduler to run in the cloud (instead of local machine)
- Add data validation/alerting for scraping failures

---

## 👤 Author

Built by **M.Jaba priyan** as a personal Data Analyst portfolio project.