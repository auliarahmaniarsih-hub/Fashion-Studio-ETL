# Fashion-Studio-ETL
Built an end-to-end ETL pipeline with web scraping, data transformation, and data loading to CSV, PostgreSQL, and Google Sheets, fully tested with pytest.

---

## 🚀 Features

- 🔎 **Web Scraping (Extract)**
  - Scrapes product data from a multi-page website
  - Handles pagination automatically
  - Uses `requests` and `BeautifulSoup`

- 🔄 **Data Transformation (Transform)**
  - Cleans and formats raw data
  - Converts price and rating into structured formats
  - Removes invalid and duplicate data

- 💾 **Data Storage (Load)**
  - Save to CSV
  - Save to PostgreSQL
  - Upload to Google Sheets

- 🧪 **Testing**
  - Unit tests with `pytest`
  - Mocking for HTTP requests and external services
  - Test coverage ~87%

---
