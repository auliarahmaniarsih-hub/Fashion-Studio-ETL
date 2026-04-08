import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_postgres, save_to_google_sheets


def test_save_to_csv(tmp_path):
    """
    Test saving dataframe to CSV file
    """

    df = pd.DataFrame({
        "Title": ["Hoodie"],
        "Price": [100000],
        "Rating": [4],
        "Colors": [5],
        "Size": ["M"],
        "Gender": ["Men"],
        "Timestamp": [pd.Timestamp("2024-01-01")]
    })

    file_path = tmp_path / "test_products.csv"

    save_to_csv(df, file_path)

    assert file_path.exists()


@patch("utils.load.psycopg2.connect")
def test_save_to_postgres(mock_connect):
    """
    Test PostgreSQL saving using mock connection
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    df = pd.DataFrame({
        "Title": ["Test Product"],
        "Price": [100],
        "Rating": [4.5],
        "Colors": ["Red"],
        "Size": ["M"],
        "Gender": ["Men"],
        "Timestamp": [pd.Timestamp("2024-01-01")]
    })

    save_to_postgres(df)

    mock_connect.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_conn.commit.assert_called_once()


@patch("utils.load.build")
def test_save_to_google_sheets(mock_build):
    """
    Test Google Sheets saving using mock API
    """

    mock_service = MagicMock()
    mock_build.return_value = mock_service

    df = pd.DataFrame({
        "Title": ["Test Product"],
        "Price": [100],
        "Rating": [4.5],
        "Colors": ["Red"],
        "Size": ["M"],
        "Gender": ["Men"],
        "Timestamp": [pd.Timestamp("2024-01-01")]
    })

    save_to_google_sheets(df, "test_sheet_id")

    mock_build.assert_called_once()