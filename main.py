from utils.extract import main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgres, save_to_google_sheets

BASE_URL = "https://fashion-studio.dicoding.dev"

print("Extracting data...")
data = main()

print("Transforming data...")
df_clean = transform_data(data)

print("Saving to CSV...")
save_to_csv(df_clean)

print("Saving to PostgreSQL...")
save_to_postgres(df_clean)

print("Saving to Google Sheets...")
save_to_google_sheets(
    df_clean,
    spreadsheet_id="17kM8s0lC686oaWTMrEXEhrtiTp9K3GJZCuoPNfd7JWk"
)

print("ETL process finished.")