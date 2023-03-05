import requests
from bs4 import BeautifulSoup
import re

# Extract car title
def get_title(pre_soup):
    car_title = pre_soup.find('h1', {'data-testid': 'ad-detail-header'}).text.strip()
    if car_title:
        return car_title
    print("No car title found!")

# Extract price
def get_price(pre_soup):
    price_element = pre_soup.find('span', {'data-testid': 'contact-box-price-box-price-value-0'})
    if price_element:
        price = price_element.text.strip()
        return price
    print("No price-element found!")

# Extract location
def get_location(pre_soup):
    location_div = pre_soup.find("div", {"data-testid": "top-contact-box-address-box"})
    if location_div:
        location_spans = location_div.find_all("span", {"class": "Text-sc-10o2fdq-0 kTmUzk"})
        location = ""
        for span in location_spans:
            text = span.text.strip()
            if text:
                location += text + " "
        if location:
            print(f"Location: {location}")
            return location
        else:
            print("No location found")
    else:
        print("No location found")

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
    else:
        print("No attribute matches")

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
    else:
        print("No equipment found")