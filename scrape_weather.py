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

print(df.head(20))      # first 20 rows
print(f"Total rows: {len(df)}")