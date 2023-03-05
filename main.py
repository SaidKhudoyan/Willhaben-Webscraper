import requests
import csv
import time
from tqdm import tqdm

from bs4 import BeautifulSoup
from OneCar import get_title, get_price, get_location, get_cardata, get_equipment

URL_1 = "SomeURL"
URL_2 = "SomeURL2"
URL_3 = "SomeURL3"

EXAMPLE_URLS = [URL_1, URL_2, URL_3]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# write the data to a CSV file
with open('willhaben_cars.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Title', 'Price', 'Location', 'BasicsData', 'Equipment'])
    for url_ in tqdm(EXAMPLE_URLS):

        RESPONSE = requests.get(url_, headers=HEADERS)
        soup_content = BeautifulSoup(RESPONSE.content, 'html.parser')

        car_title = get_title(soup_content)
        car_price = get_price(soup_content)
        car_location = get_location(soup_content)
        car_data = get_cardata(soup_content)
        car_equipment = get_equipment(soup_content)

        writer.writerow([car_title, car_price, car_location, car_data, car_equipment])
        time.sleep(1)

