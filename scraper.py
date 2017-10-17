import pprint
import re
import requests
import sys
from bs4 import BeautifulSoup

def fetch_search_results(
    query=None, minAsk=None, maxAsk=None, bedrooms=None
):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError('No valid keywords')

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status() # <- no-op if status==200
    return resp.content, resp.encoding

def extract_listings(parsed):
    listings = parsed.find_all('li', class_='result-row')
    extracted = []
    for i, listing in enumerate(listings):
        link = listing.find('a', class_='result-title')
        price = listing.find('span', class_='result-price')
        this_listing = {
            'description': link.string.strip(),
            'link': link.attrs['href']
        }
        extracted.append(this_listing)
    return extracted

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, 'html.parser', from_encoding=encoding)
    return parsed

def read_search_results():
    with open('apartments.html', 'rb') as f:
        html = f.read()
    return html, 'utf-8'

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(
            minAsk=1200, maxAsk=1800, bedrooms=1
        )
    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    print(len(listings))
    pprint.pprint(listings[0])


def match_listings(tag):
    return tag.get_attribute_list('class') == ['result-row'] and \
           len(tag.find_all('span', class_='housing')) > 0

def parse_housing(housing):
    rooms, sqft = re.findall('[a-zA-Z0-9]+', housing)
    return rooms, sqft
