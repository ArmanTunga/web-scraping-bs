import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1000)

url = "https://www.remax.com.tr/konut?currency=1&country=1"
soup = BeautifulSoup(html_doc, 'html.parser')