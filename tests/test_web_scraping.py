import unittest
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import json
from proxy_requests import ProxyRequests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests

property24_url = "https://www.property24.com"
# Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0

headers = {
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
 }


# Target web page
class TestWebScraping(unittest.TestCase):

    # Need the selenium driver matching the browser installed
    def test_scrape_search_results(self):
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.get("https://www.property24.com/for-sale/knysna-rural/knysna/western-cape/16620?sp=bd%3d4%26hp%3dTrue&PropertyCategory=House%2cApartmentOrFlat%2cTownhouse%2cFarm")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        with open('search_results.html', 'w') as fout:
            fout.write(driver.page_source)

        links = []
        properties_on_page = soup.find_all('div', class_='p24_regularTile')
        for p in properties_on_page:
            if not 'data-group-list-id' in p.attrs:
                for link in p.find_all('a', class_=''):
                    href = property24_url + link.attrs["href"]
                    title = link.attrs["title"] if "title" in link.attrs else ""
                    links.append({"href": href, "title": title, "search": "wellington-rural", "page": 1})

        with open('search_results.json', 'w') as fout:
            json.dump(links, fout)

    # This got my IP address blocked by Property 24 - maybe it looked like a DoS??
    def test_scrape_search_results___requests_version(self):
        url = "https://www.property24.com/for-sale/knysna-rural/knysna/western-cape/16620?sp=bd%3d4%26hp%3dTrue"
        response = requests.get(url, headers=headers)
        print(response.status_code)
        sleep(randint(1, 5))
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        properties_on_page = soup.find_all('div', class_='p24_regularTile')
        for p in properties_on_page:
            for link in p.find_all('a'):
                href = property24_url + link.attrs["href"]
                title = link.attrs["title"] if "title" in link.attrs else ""
                links.append({"href": href, "title": title, "search": "wellington-rural", "page": 1})

        with open('search_results.json', 'w') as fout:
            json.dump(links, fout)

    def test_scrape_individual_farms(self):
        links = []
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        with open(r"search_results.json", "r") as read_file:
            links = json.load(read_file)

        for link in links:
            sleep(randint(1, 5))

            driver.get(link["href"])
            p = BeautifulSoup(driver.page_source, 'html.parser')

            # take the 2nd element - first isn't populated by the
            price = p.find_all("div", class_="p24_price")[1].text if len(p.find_all("div", class_="p24_price")) > 1 else ""
            link["price"] = price

            address = p.find_all("a", class_="p24_address")[0].text if len(p.find_all("a", class_="p24_address")) > 0 else ""
            link["address"] = address

            size = p.find_all("a", class_="js_sizeConversionsButton")[0].text.strip() if len(p.find_all("a", class_="js_sizeConversionsButton")) > 0 else ""
            link["size"] = size

            # TODO - iterate over the features taking each and converting to an attribute
            features = p.find_all("div", "p24_listingFeatures")
            for feature in features:
                feature_key = feature.find_all("span", "p24_feature")[0].text.replace(":", "")
                feature_value = feature.find_all("span", "p24_featureAmount")[0].text if len(feature.find_all("span", "p24_featureAmount")) > 0 else ''
                link[feature_key] = feature_value

            read_more_text = p.find_all("div", class_="p24_readMoreText")[0].text if len(p.find_all("div", class_="p24_readMoreText")) > 0 else ""
            link["read_more_text"] = read_more_text

            about_div = p.find_all("div", class_="p24_listingAbout")
            about_title = about_div[0].find_all("h5")[0].text if len(about_div) > 0 and len(about_div[0].find_all("h5")) > 0 else ""
            link["about_title"] = about_title

        with open('farms.json', 'w') as fout:
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
