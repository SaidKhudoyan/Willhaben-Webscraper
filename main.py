import requests
import csv
import time
import Get_Cars
import os

from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

#####################################################################
# PARAMETERS TO BE CHANGED
TEST_URL = "https://www.willhaben.at/iad/gebrauchtwagen/auto/audi-gebrauchtwagen"
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse'
    }

TAR_PATH = "/WILL_SCRAPER/CAR_CSVs/"
MAX_PAGES = 3 # maximum number of pages to scrape the urls, usually 30 cars per page, if set to "INF", it will get all data until the last page
####################################################################

if not os.path.exists(TAR_PATH):
    os.makedirs(TAR_PATH)

print("GET URL'S.....")
EXAMPLE_URLS = Get_Cars.get_urls(TEST_URL, HEADERS=HEADERS, MAX_PAGES=MAX_PAGES)

NOW = datetime.now()
dt_string = NOW.strftime("%d_%m_%Y_%H_%M_%S")
filename = f"Willhaben_CARS_{dt_string}.csv"
filepath = os.path.join(TAR_PATH, filename)
print(f"CREATED NEW FILE: {filepath}.....")

with open(filepath, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Title', 'Price', 'Location', "Erstzulassung", "Kilometerstand", "Leistung", "Treibstoff", "Getriebeart", "Fahrzeugtyp", "Vorbesitzer", "Zustand", 'BasicsData', 'Equipment'])

    print("EXTRACT DATA.....")
    for url_ in tqdm(EXAMPLE_URLS):
        with requests.Session() as session:
            RESPONSE = session.get(url_, headers=HEADERS)
            soup_content = BeautifulSoup(RESPONSE.content, 'html.parser')
            if not RESPONSE or not soup_content:
                print("Response or soup_content is None.")
            else:
                car_title = Get_Cars.get_title(soup_content)
                car_price = Get_Cars.get_price(soup_content)
                car_location = Get_Cars.get_location(soup_content)
                car_data = Get_Cars.get_cardata(soup_content)
                if car_data:
                    Erstzulassung = car_data.get("Erstzulassung", "NaN")
                    Kilometerstand = car_data.get("Kilometerstand", "NaN")
                    Leistung = car_data.get("Leistung", "NaN")
                    Treibstoff = car_data.get("Treibstoff", "NaN")
                    Getriebeart = car_data.get("Getriebeart", "NaN")
                    Fahrzeugtyp = car_data.get("Fahrzeugtyp", "NaN")
                    Vorbesitzer = car_data.get("Vorbesitzer", "NaN")
                    Zustand = car_data.get("Zustand", "NaN")
                car_equipment = Get_Cars.get_equipment(soup_content)
        
        key_to_remove = ["Erstzulassung", "Kilometerstand", "Leistung", "Treibstoff", "Getriebeart", "Fahrzeugtyp", "Vorbesitzer", "Zustand"]
        for i in key_to_remove:
            try:
                car_data.pop(i)
            except KeyError:
                continue
        writer.writerow([car_title, car_price, car_location, Erstzulassung, Kilometerstand, Leistung, Treibstoff, Getriebeart, Fahrzeugtyp, Vorbesitzer, Zustand ,car_data, car_equipment])
        time.sleep(0.1)