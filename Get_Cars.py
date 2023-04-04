import requests
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

# Extract car title
def get_title(pre_soup):
    car_title = pre_soup.find('h1', {'data-testid': 'ad-detail-header'}).text.strip()
    if car_title:
        return car_title
    print("No car title found!")
    return "NaN"

# Extract price
def get_price(pre_soup):
    price_element = pre_soup.find('span', {'data-testid': 'contact-box-price-box-price-value-0'})
    if price_element:
        price = price_element.text.strip()
        return price
    print("No price-element found!")
    return "NaN"

# Extract location
def get_location(pre_soup):
    location_div = pre_soup.find("div", {"data-testid": "top-contact-box-address-box"})
    if location_div:
        location_spans = location_div.find_all("span", {"class": "Text-sc-10o2fdq-0 iyWCfU"})
        location = ""
        for span in location_spans:
            text = span.text.strip()
            if text:
                location += text + " "
        if location:
            return location
        print("No location found")
        return "NaN"
    print("No location found")
    return "NaN"

# Extract Cardata
def get_cardata(pre_soup):
    basis_daten = pre_soup.find_all('li', {'data-testid': 'attribute-item'})

    if basis_daten:
        cardata_dict = {}
        for item in basis_daten:
            title = item.find('div', {'data-testid': 'attribute-title'}).span.text
            value = item.find('div', {'data-testid': 'attribute-value'}).text
            cardata_dict[title] = value
        return cardata_dict
    print("No attribute matches")
    return {}

# Extract Ausstattungen & Extras
def get_equipment(pre_soup):
    equipment_items = pre_soup.find_all('li', {'data-testid': 'equipment-item'})
    all_equipments = []
    if equipment_items:
        for item in equipment_items:
            equip_value = item.find('div', {'data-testid': 'equipment-value'})
            if equip_value:
                equip_text = equip_value.text.strip()
                all_equipments.append(equip_text)
        return all_equipments
    print("No equipment found")
    return "NaN"


# Extract URL's from Willhaben
def get_urls(url, params={}, HEADERS="something", MAX_PAGES = 1):
    # Initialize page counter
    url_list = []
    count = 1
    with requests.Session() as session:
        # Get the first page
        print("-"*20)
        print(f"Get URL's from page {count}")
        print("-"*20)
        response = session.get(url, params={"page": 1}, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = soup.select('script[type="application/ld+json"]')[0].string
        urls = [item["url"] for item in json.loads(urls)["itemListElement"]]
        for ele_url in urls:
            url_list.append(ele_url)

        # Get the rest of the pages
        while True:
            count += 1
            params['page'] = count
            response = session.get(url, params=params, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            urls = soup.select('script[type="application/ld+json"]')[0].string
            urls = [item["url"] for item in json.loads(urls)["itemListElement"]]
            if not urls or (MAX_PAGES != "INF" and count > MAX_PAGES):
                break
            print("-"*20)
            print(f"Get URL's from page {count}")
            print("-"*20)
            for ele_url in urls:
                url_list.append(ele_url)
        full_urls = []
        for element in url_list:
            full_urls.append("https://www.willhaben.at"+element)
        print(f"We got {len(full_urls)} urls!")
    return full_urls
