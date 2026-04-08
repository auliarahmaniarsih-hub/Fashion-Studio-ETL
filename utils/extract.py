import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

session = requests.Session()

def fetching_content(url):
    """Fetching HTML content from given URL."""
    response = session.get(url, headers=HEADERS, timeout=10)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Some error occurred while fetching {url}: {e}")
        return None

def extract_product_data(article):

    title_element = article.find("h3", class_="product-title")
    title = title_element.text.strip() if title_element else None

    price_element = article.find("span", class_="price")
    price = price_element.text.strip() if price_element else None

    paragraphs = article.find_all("p")

    rating = paragraphs[0].text.strip() if len(paragraphs) > 0 else None
    colors = paragraphs[1].text.strip() if len(paragraphs) > 1 else None
    size = paragraphs[2].text.strip() if len(paragraphs) > 2 else None
    gender = paragraphs[3].text.strip() if len(paragraphs) > 3 else None

    product = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Timestamp": datetime.now()
    }

    return product

def scrape_products(base_url, delay=2):
    """Main function to scrape product data from the Fashion Studio website."""
    
    data = []
    url = base_url
 
    while url:
        print(f"Scraping: {url}")

        content = fetching_content(url)

        if not content:
            break

        soup = BeautifulSoup(content, "html.parser")

        products = soup.find_all("div", class_="product-details")

        for product in products:
            product_data = extract_product_data(product)
            data.append(product_data)

        next_button = soup.find("a", string="Next")

        if next_button:
            BASE_DOMAIN = "https://fashion-studio.dicoding.dev"
            url = BASE_DOMAIN + next_button["href"]
            time.sleep(delay)
        else:
            url = None

    return data
 
 
def main():
    """Main function to execute the scraping process."""
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    all_products_data = scrape_products(BASE_URL)
    df = pd.DataFrame(all_products_data)

    print(df)
    
    df.to_csv("products.csv", index=False)
    print("Data successfully saved to products.csv")

    return df

 
 
if __name__ == '__main__':
    main()