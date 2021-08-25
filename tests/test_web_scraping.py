import unittest
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import json
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests

property24_url = "https://www.property24.com"
# Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

#sub_area = "knysna-rural"
#area = "knysna"
#region = "western-cape"
#area_code = "16620"

#sub_area = "wellington-rural"
#area = "wellington"
#region = "western-cape"
#area_code = "16608"

sub_area = "plettenberg-bay-rural"
area = "plettenberg-bay"
region = "western-cape"
area_code = "16621"

SCROLL_PAUSE_TIME = 2.0


# Target web page
class TestWebScraping(unittest.TestCase):

    # Need the selenium driver matching the browser installed
    def test_scrape_search_results(self):

        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        url = f"https://www.property24.com/for-sale/{sub_area}/{area}/{region}/{area_code}?PropertyCategory=Farm"
        driver.get(url)

        links = []

        result_count_raw = driver.find_elements_by_xpath("//*[contains(text(), 'Showing :')]")[0].text
        result_count_parsed = int(re.sub(r'Showing : 1 - (.*) of ', "", result_count_raw))
        # 20 results per page by default
        page_count = int(min(result_count_parsed / 20, 5)) + 1
        page_suffixes = ['', '/p2', '/p3', '/p4']
        for page_number in range(0, page_count):
            page_suffix = page_suffixes[page_number]
            url = f"https://www.property24.com/for-sale/{sub_area}/{area}/{region}/{area_code}{page_suffix}"
            driver.get(url)

            with open(f'search_results_{sub_area}_{area}_{region}_{area_code}{page_suffix.replace("/", "_")}.html',
                      'w') as fout:
                fout.write(driver.page_source)

            tile_divs = driver.find_elements_by_class_name("p24_regularTile")

            for tile in tile_divs:
                if tile.is_displayed():
                    if len(tile.find_elements_by_tag_name('a')) > 0:
                        listing_image_lazy_src = tile.find_element_by_class_name('js_P24_listingImage').get_attribute(
                            "lazy-src")
                        listing_image_src = tile.find_element_by_class_name('js_P24_listingImage').get_attribute("src")
                        listing_image = listing_image_src if listing_image_src != "https://www.property24.com/blank.gif" else listing_image_lazy_src
                        anchor_tag = tile.find_element_by_tag_name('a')
                        href = anchor_tag.get_attribute("href")
                        title = anchor_tag.get_attribute("title")
                        links.append({"href": href, "title": title, "listing_image": listing_image, "search": sub_area,
                                      "page": 1})

        with open(f'search_results_{sub_area}_{area}_{region}_{area_code}.json', 'w') as fout:
            json.dump(links, fout)

    def test_scrape_individual_farms(self):
        links = []
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        with open(f'search_results_{sub_area}_{area}_{region}_{area_code}.json', "r") as read_file:
            links = json.load(read_file)

        for link in links:
            sleep(randint(1, 5))

            driver.get(link["href"])
            p = BeautifulSoup(driver.page_source, 'html.parser')

            # take the 2nd element - first isn't populated by the
            price = p.find_all("div", class_="p24_price")[1].text if len(
                p.find_all("div", class_="p24_price")) > 1 else ""
            link["price"] = price

            address = p.find_all("a", class_="p24_address")[0].text if len(
                p.find_all("a", class_="p24_address")) > 0 else ""
            link["address"] = address

            size = p.find_all("a", class_="js_sizeConversionsButton")[0].text.strip() if len(
                p.find_all("a", class_="js_sizeConversionsButton")) > 0 else ""
            link["size"] = size

            # TODO - iterate over the features taking each and converting to an attribute
            features = p.find_all("div", "p24_listingFeatures")
            for feature in features:
                feature_key = feature.find_all("span", "p24_feature")[0].text.replace(":", "")
                feature_value = feature.find_all("span", "p24_featureAmount")[0].text if len(
                    feature.find_all("span", "p24_featureAmount")) > 0 else 'true'
                link[feature_key] = feature_value

            read_more_text = p.find_all("div", class_="p24_readMoreText")[0].text if len(
                p.find_all("div", class_="p24_readMoreText")) > 0 else ""
            link["read_more_text"] = read_more_text

            about_div = p.find_all("div", class_="p24_listingAbout")
            about_title = about_div[0].find_all("h5")[0].text if len(about_div) > 0 and len(
                about_div[0].find_all("h5")) > 0 else ""
            link["about_title"] = about_title

        with open(f'properties_{sub_area}_{area}_{region}_{area_code}.json', 'w') as fout:
            json.dump(links, fout)

    def test_example_scrape(self):

        # Connection to web page
        url = "https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html"
        response = requests.get(url)
        print(response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all h1 tags
        h1_tags = soup.find_all('h1')

        # Should have 2x h1 tags
        self.assertEqual(len(h1_tags), 2)

        # Find all elements that have 'company' class
        company = soup.find_all(class_="company")

        # should have 1 company tags
        self.assertEqual(company[0].contents[0], "Payne, Roberts and Davis")
