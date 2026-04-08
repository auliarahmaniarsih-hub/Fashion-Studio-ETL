import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def save_to_csv(df, filename="clean_products.csv"):
    try:
        df.to_csv(filename, index=False)
        print("Data successfully saved to CSV.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def save_to_postgres(df):
    df =df.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    try:
        conn = psycopg2.connect(
                host="aws-1-ap-northeast-2.pooler.supabase.com",
                database="postgres",
                user="postgres.zzkrpfadkkcokvbrpkrz",
                password="supersecretpassword123%",
                port=6543,
                sslmode="require"
        )
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
            title TEXT,
            price FLOAT,
            rating FLOAT,
            colors TEXT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
            )
            """
        )

        # Insert data into the table   
        for _, row in df.iterrows():
            cursor.execute(
            """
            INSERT INTO products (title, price, rating, colors, size, gender, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["Title"],
                row["Price"],
                row["Rating"],
                row["Colors"],
                row["Size"],
                row["Gender"],
                row["Timestamp"]
            ),
        )

        conn.commit()
        print("Data successfully saved to PostgreSQL.")

    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def save_to_google_sheets(df, spreadsheet_id, range_name="Sheet1!A1"):
    df =df.copy()
    df["Timestamp"] = df["Timestamp"].astype(str)
    try:
        creds = Credentials.from_service_account_file(
        "google-sheets-api.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        service = build("sheets", "v4", credentials=creds)

        values = [df.columns.tolist()] + df.values.tolist()

        body = {
            "values": values
        }

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        print("Data successfully saved to Google Sheets.")

    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")