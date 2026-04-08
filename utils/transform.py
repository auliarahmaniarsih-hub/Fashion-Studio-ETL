import pandas as pd
from datetime import datetime

def transform_data(df):

    # remove invalid product names
    df = df[df["Title"] != "Unknown Product"]

    # remove duplicates
    df = df.drop_duplicates()

    # clean price
    df["Price"] = (
        df["Price"]
        .str.replace("$", "", regex=False)
        .astype(float) * 16000
    )

    # clean rating
    df["Rating"] = (
    df["Rating"]
    .str.extract(r'(\d+\.\d+|\d+)')  # fetching decimal or integer numbers
    .astype(float)
)

    # clean colors
    df["Colors"] = (
        df["Colors"]
        .str.extract(r"(\d+)")
        .fillna(0)
        .astype(int)
        )

    # clean size
    df["Size"] = df["Size"].str.replace("Size: ", "", regex=False)

    # clean gender
    df["Gender"] = df["Gender"].str.replace("Gender: ", "", regex=False)

    # transform timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # remove null values
    df = df.dropna()

    try:
        df["Price"] = df["Price"].astype(float)
        df["Rating"] = df["Rating"].astype(float)
        df["Colors"] = df["Colors"].astype(int)
        df["Size"] = df["Size"].astype(str)
        df["Gender"] = df["Gender"].astype(str)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    except Exception as e:
        print(f"Error transforming data types: {e}")

    return df