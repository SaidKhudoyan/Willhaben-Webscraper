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

TAR_PATH = "/home/said/PycharmProjects/WILL_SCRAPER/CAR_CSVs/"
MAX_PAGES = 10 # maximum number of pages to scrape the urls, usually 30 cars per page, if set to "INF", it will get all data until the last page

# DO NOT CHANGE
CSV_COLUMNS_TITLE = ['Title', 'Price', 'Location', "Erstzulassung", "Kilometerstand", "Leistung", "Treibstoff", "Getriebeart", "Fahrzeugtyp", "Vorbesitzer", 
               "Zustand", "Antrieb", "CO₂-Ausstoß", "Verbrauch", "Anzahl Türen", "Anzahl Sitze" , 'RestAttributes', 'Equipment']
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
    writer.writerow(CSV_COLUMNS_TITLE)
    print("EXTRACT DATA.....")
    for url_ in tqdm(EXAMPLE_URLS):
        with requests.Session() as session:
            try:
                RESPONSE = session.get(url_, headers=HEADERS)
                soup_content = BeautifulSoup(RESPONSE.content, 'html.parser')
            except Exception("Invalid URL encountered. SKIP to next URL."):
                continue
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
                    Antrieb = car_data.get("Antrieb", "NaN")
                    CO2_Ausstoß = car_data.get("CO₂-Ausstoß", "NaN")
                    Verbrauch = car_data.get("Verbrauch", "NaN")
                    AnzahlTüren = car_data.get("Anzahl Türen", "NaN")
                    AnzahlSitze = car_data.get("Anzahl Sitze", "NaN")
                car_equipment = Get_Cars.get_equipment(soup_content)
        
                for i in CSV_COLUMNS_TITLE:
                    try:
                        car_data.pop(i)
                    except KeyError:
                        continue
                writer.writerow([car_title, car_price, car_location, Erstzulassung, Kilometerstand, Leistung, Treibstoff, Getriebeart, Fahrzeugtyp, Vorbesitzer, 
                                 Zustand, Antrieb, CO2_Ausstoß, Verbrauch, AnzahlTüren, AnzahlSitze, car_data, car_equipment])
                time.sleep(0.1)