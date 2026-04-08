import pandas as pd
from utils.transform import transform_data


def test_transform_removes_invalid_and_duplicates():

    data = {
        "Title": ["Hoodie", "Unknown Product", "Hoodie"],
        "Price": ["$10", "$20", "$10"],
        "Rating": ["Rating: ⭐⭐⭐ / 5", "Rating: ⭐⭐ / 5", "Rating: ⭐⭐⭐ / 5"],
        "Colors": ["5 Colors", "3 Colors", "5 Colors"],
        "Size": ["Size: M", "Size: L", "Size: M"],
        "Gender": ["Gender: Men", "Gender: Women", "Gender: Men"],
        "Timestamp": ["2024-01-01", "2024-01-02", "2024-01-01"]
    }

    df = pd.DataFrame(data)

    df_clean = transform_data(df)

    assert "Unknown Product" not in df_clean["Title"].values
    assert df_clean.duplicated().sum() == 0
    assert df_clean.isnull().sum().sum() == 0


def test_price_conversion():

    data = {
        "Title": ["Hoodie"],
        "Price": ["$10"],
        "Rating": ["Rating: ⭐⭐⭐ / 5"],
        "Colors": ["5 Colors"],
        "Size": ["Size: M"],
        "Gender": ["Gender: Men"],
        "Timestamp": ["2024-01-01"]
    }

    df = pd.DataFrame(data)

    df_clean = transform_data(df)

    assert df_clean["Price"].iloc[0] == 160000