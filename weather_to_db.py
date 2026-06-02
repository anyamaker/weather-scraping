import pandas as pd
import sqlite3
import os

# Path to cleaned CSV
csv_file = "weather_all_cities.csv"  # or "weather_cleaned.csv"
db_path = "weather.db"

# Read CSV
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows from {csv_file}")

# Connect to SQLite database
conn = sqlite3.connect(db_path)

# Write to table (replace if exists)
df.to_sql("weather_data", conn, if_exists="replace", index=False)
print(f"Saved to {db_path} as table 'weather_data'")

# Verify
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM weather_data")
count = cursor.fetchone()[0]
print(f"Table has {count} rows")

conn.close()