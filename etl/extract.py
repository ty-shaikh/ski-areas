"""Data Extraction

This script scrapes data from Ski Central's website.

The script takes in website URLs and outputs a pickle file.

This script requires that 'requests' and 'bs4' be installed within the
local Python environment.
"""

import time
import pickle

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.skicentral.com/"
RESORT_URL = "resorts.html"
region_ids = ["useast_tabs", "usmidatlantic_tabs", "uswest_tabs", "usmidwest_tabs", "canada_tabs"]

def get_resorts_page():
    """Downloads the website and parses the resorts page

    Parameters
    ----------
    None

    Returns
    -------
    BeautifulSoup
        A BeautifulSoup object the represents the parsed resorts page
    """
    page_url = BASE_URL + RESORT_URL
    page = requests.get(page_url, verify=True)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def extract_region_links(soup: BeautifulSoup, region_id: str):
    """Extracts all the region names and link references from the resorts page

    Parameters
    ----------
    soup : BeautifulSoup
        The object that represents the parsed webpage
    region_id : str
        The string that represents the HTML id for the region component

    Returns
    -------
    store
        A dictionary that contains the region name and link reference
    """

    html_block = soup.find(id=region_id)
    a_tags = html_block.find_all("a")
    links = [link['href'] for link in a_tags]
    return links

def get_region_page(region_url: str):
    """Downloads and parses the region website

    Parameters
    ----------
    region_url : str
        A URL for the ski region

    Returns
    -------
    BeautifulSoup
        A BeautifulSoup object the represents the parsed ski table
    """
    page_url = BASE_URL + region_url
    page = requests.get(page_url, verify=True)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def extract_area_links(soup: BeautifulSoup):
    """Extracts the link name and reference from the ski table

    Parameters
    ----------
    soup : BeautifulSoup
        The object that represents the parsed webpage

    Returns
    -------
    store
        A dictionary that contains the mountain name and href value
    """
    link_elements = [item.find('a') for item in soup.find_all(class_="resorttitle")]
    links = [link['href'] for link in link_elements]
    return links

def get_area_page(area_url: str):
    """Downloads the website and parses the ski page

    Parameters
    ----------
    area_url : str
        A URL for the ski area

    Returns
    -------
    BeautifulSoup
        A BeautifulSoup object the represents the parsed ski page
    """
    time.sleep(5)
    page_url = BASE_URL + area_url
    page = requests.get(page_url, verify=True)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def extract_stats(soup: BeautifulSoup):
    """Extracts the text data from the webpage

    Parameters
    ----------
    soup : BeautifulSoup
        The object that represents the parsed webpage

    Returns
    -------
    store
        A dictionary that contains the mountain statistics names and values
    """
    store = {}

    try:
        name_block = soup.find(class_='resortname')
        name = name_block.text
        store['Name'] = name
    except:
        store['Name'] = ''

    try:
        address_block = soup.find(class_='addressblock')
        address = address_block.text
        store['Address'] = address
    except:
        store['Address'] = ''

    table = soup.find(id='mountainstatistics').find_all('tr')
    for row in table[:8]:
        name, value = row.find_all('td')
        name = name.text
        value = value.text
        store[name] = value

    return store

def main():
    print("Running the extract script")
    resorts_page = get_resorts_page()
    lists_of_region_links = [extract_region_links(resorts_page, id) for id in region_ids]
    region_links = sum(lists_of_region_links, [])

    # Slice region_links for faster_testing
    region_pages = [get_region_page(link) for link in region_links[:2]]
    lists_of_area_links = [extract_area_links(page) for page in region_pages]
    area_links = sum(lists_of_area_links, [])

    # Slice area_links for faster testing
    area_pages = [get_area_page(link) for link in area_links[:5]]
    raw_data = [extract_stats(page) for page in area_pages]

    pickle.dump(raw_data, open('./data/extract_output.pkl', 'wb'))
    print("The raw data has been extracted")

if __name__ == "__main__":
    main()
