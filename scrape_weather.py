from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.timeanddate.com/weather/")
time.sleep(3)

results = []
i = 0
while True:
    try:
        cell = driver.find_element(By.ID, f"p{i}")
    except:
        break
    row = cell.find_element(By.XPATH, "./ancestor::tr")
    city = row.find_element(By.CSS_SELECTOR, "td a").text.strip()
    temp = row.find_element(By.CLASS_NAME, "rbi").text.strip()
    day_time = cell.text.strip()
    condition = "N/A"
    for rc in row.find_elements(By.CLASS_NAME, "r"):
        if rc == cell:
            continue
        try:
            img = rc.find_element(By.TAG_NAME, "img")
            condition = img.get_attribute("title")
            break
        except:
            pass
    results.append({"City": city, "Temperature": temp, "Day & Time": day_time, "Condition": condition})
    i += 1

driver.quit()
df = pd.DataFrame(results)
df.to_csv("weather_all_cities.csv", index=False)

# --- Data Cleaning ---
# Remove duplicate cities
df = df.drop_duplicates(subset="City", keep="first")

# Extract numeric temperature (remove "°F" and convert to integer)
df['Temp_F'] = df['Temperature'].str.replace(' °F', '').astype(int)

# Extract day and time from "Day & Time" column
df['Day'] = df['Day & Time'].str.split().str[0]
df['Time'] = df['Day & Time'].str.split(n=1).str[1]

# Remove any rows with missing critical data
df = df.dropna(subset=['City', 'Temp_F'])

# Reorder columns
df = df[['City', 'Temp_F', 'Day', 'Time', 'Condition']]

# Save cleaned version
df.to_csv("weather_cleaned.csv", index=False)
print(f"Cleaned data: {len(df)} cities")
print(df.head(20))      # first 20 rows