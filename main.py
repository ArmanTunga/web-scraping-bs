import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1000)

url = "https://www.remax.com.tr/konut?currency=1&country=1"
response = requests.get(url)
if response.status_code == 200:
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    soup.prettify()

    for i in range(200):
        # Get results div
        result_div = soup.find("div", class_="result-list")

        # Get all listings
        listings = result_div.find_all("div", class_="item")

        # Extract detail page urls of listings
        listing_urls = []
        for item in listings:
            a_element = item.find("a")
            listing_urls.append(a_element["href"])
        BASE_URL = "https://www.remax.com.tr"

        # Scrape detail pages of listings
        data = []
        for detail_url in listing_urls:
            detail_url = f"{BASE_URL}{detail_url}"
            response = requests.get(detail_url)
            if response.status_code == 200:
                html_doc = response.content
                soup = BeautifulSoup(html_doc, 'html.parser')
                page_title = soup.title
                page_title = page_title.text
                properties_div = soup.find("div", class_="properties")
                price = properties_div.find("strong")
                price = price.text
                price = price.split(" ")[0]
                ul_element = properties_div.find("ul")
                attribute_elements = ul_element.find_all("li")
                row = {"Fiyat": price}
                for element in attribute_elements:
                    """
                    if variable is None:
                        continue      
                    variable = variable.text
                    """
                    variable = element.find("strong").text
                    value = element.find("span").text
                    row[variable] = value
                data.append(row)

    len(data)
    df = pd.DataFrame(data)
    df.head()
    df.describe().T
else:
    print("Couldn't get the page, status code is not 200")

# TODO
#   Add try except or if object statement (better than try-except)
#   EDA Process
#   Data visualization
#   Make a function called "scrape_detail_page" (optional)
#   Add scrape all pages option using while or for i in range loops.
