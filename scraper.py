import pprint
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
    for listing in listings:
        link = listing.find('a', class_='result-title')
        price = listing.find('span', class_='result-price')
        housing = listing.find('span',  class_='housing')
        if housing != None:
            print("We're good")
        else:
            print('Uh-oh')
            pprint.pprint(listing)

        this_listing = {
            'description': link.string.strip(),
            'link': link.attrs['href'],
            'housing': list(housing.children)[0],
        }
        extracted.append(this_listing)
        # import  pdb; pdb.set_trace() # TODO: TEMPORARY BREAKPOINT
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
    # print(doc.prettify(encoding=encoding))
    print(len(listings))
    # print(listings[0].prettify())
    pprint.pprint(listings[0])
