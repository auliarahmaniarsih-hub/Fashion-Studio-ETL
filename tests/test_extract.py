import pytest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import scrape_products, extract_product_data, fetching_content

fake_html = """
<html>
<body>
<div class="product-details">
    <h3 class="product-title">Hoodie</h3>
    <span class="price">$100</span>
    <p>4.5</p>
    <p>5 colors</p>
    <p>M</p>
    <p>Men</p>
</div>
</body>
</html>
"""

# Main Scraping Function Tests
@patch("utils.extract.time.sleep", return_value=None)
@patch("utils.extract.session.get")
def test_scrape_products_returns_data(mock_get, _):
    """Test scraper returns list with data"""

    mock_response = MagicMock()
    mock_response.content = fake_html.encode("utf-8")
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    data = scrape_products("https://fakeurl.com")

    assert isinstance(data, list)
    assert len(data) == 1


@patch("utils.extract.time.sleep", return_value=None)
@patch("utils.extract.session.get")
def test_scrape_products_keys(mock_get, _):
    """Test scraper returns correct product keys"""

    mock_response = MagicMock()
    mock_response.content = fake_html.encode("utf-8")
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    data = scrape_products("https://fakeurl.com")
    product = data[0]

    expected_keys = {
        "Title",
        "Price",
        "Rating",
        "Colors",
        "Size",
        "Gender",
        "Timestamp"
    }

    assert set(product.keys()) == expected_keys


# Edge Case Tests
@patch("utils.extract.session.get")
def test_fetching_content_exception(mock_get):
    """Test fetching_content handles request exception"""

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Error")

    mock_get.return_value = mock_response

    result = fetching_content("https://fakeurl.com")

    assert result is None


@patch("utils.extract.session.get")
def test_scrape_products_no_content(mock_get):
    """Test scraper handles empty content"""

    mock_response = MagicMock()
    mock_response.content = None
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    data = scrape_products("https://fakeurl.com")

    assert data == []


# Pagination Tests
@patch("utils.extract.time.sleep", return_value=None)
@patch("utils.extract.session.get")
def test_scrape_products_pagination(mock_get, _):
    """Test scraper handles multiple pages"""

    html_page1 = """
    <html><body>
    <div class="product-details">
        <h3 class="product-title">Hoodie</h3>
        <span class="price">$100</span>
        <p>4.5</p><p>5 colors</p><p>M</p><p>Men</p>
    </div>
    <a href="/page2">Next</a>
    </body></html>
    """

    html_page2 = """
    <html><body>
    <div class="product-details">
        <h3 class="product-title">Jacket</h3>
        <span class="price">$200</span>
        <p>4.0</p><p>3 colors</p><p>L</p><p>Men</p>
    </div>
    </body></html>
    """

    mock_get.side_effect = [
        MagicMock(content=html_page1.encode(), status_code=200),
        MagicMock(content=html_page2.encode(), status_code=200),
    ]

    data = scrape_products("https://fakeurl.com")

    assert len(data) == 2


# UNIT TESTS (SMALL FUNCTION)
def test_extract_product_missing_fields():
    """Test extract_product_data handles missing HTML fields"""

    html = '<div class="product-details"></div>'
    soup = BeautifulSoup(html, "html.parser")

    product = extract_product_data(soup)

    assert product["Title"] is None
    assert product["Price"] is None
    assert product["Rating"] is None