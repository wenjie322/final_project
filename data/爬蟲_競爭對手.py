import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://data.gcis.nat.gov.tw/od/data/api/F570BC9A-DA4C-4813-8087-FB9CE95F9D38?$format=json&$filter=President_No eq 15725713 and Agency eq 376610000A&$skip=0&$top=50'

with urllib.request.urlopen(url) as response:
	data = response.read().decode('utf-8')

print(data)