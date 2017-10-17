'''rentscraper.zipcodesearch
'''
import datetime
import os
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from log import get_configured_logger

class ZipCodeSearch(object):
    '''Implements a search for all rental listings by zip code.

    Attributes:
        base: base URL for the search
        city: used to complete the base URL
        logger: self explanatory
        proxy: proxy IP set by env var HTTP_PROXY
        ua: UserAgent object to generate random user agnets
        zipcode: zip code for this search

    '''

    def __init__(self, city, zipcode, mongoclient):
        self.base = os.environ['BASE_URL']
        self.city = city.lower()
        self.logger = get_configured_logger('DEBUG', __name__)
        self.mongoclient = mongoclient
        self.proxy = os.environ['HTTP_PROXY']
        self.ua = UserAgent()
        self.zipcode = zipcode

        self.logger.info(
            'ZipCodeSearch initialized for zip code {}'.format(
                self.zipcode
            )
        )

    def execute(self):
    '''Executes a zip code search for rental properties'''
        results = []
        content = self._search()
        results.append(content)
        count = self._countresults(content)
        self.logger.info(
            'Found {} results for this zip code'.format(count)
        )

        listings = self._parseresults(content)
        self._writelistingstomongo(listings)

        for s in range(120, int(count), 120):
            time.sleep(1)
            content = self._search(str(s))
            listings = self._parseresults(content, str(s))
            self._writelistingstomongo(listings)

    def _countresults(self, content):
        '''return number of results found in content'''
        soup = BeautifulSoup(content, 'html.parser')
        count = soup.select('.totalcount')[0].text
        return count

    def _parseresults(self, content, s='0'):
        listings = []
        soup = BeautifulSoup(content, 'html.parser')
        resulttitles = soup.select('.result-title.hdrlnk')
        for title in resulttitles:
            listing = {
                'link': title.attrs['href'],
                's': s,
                'timestamp': datetime.datetime.utcnow(),
                'title': title.text,
                'zipcode': self.zipcode
            }
            listings.append(listing)
        self.logger.info('Parsed {} listings'.format(len(listings)))
        return listings

    def _search(self, s=None):
        '''get a page of search results'''
        url = self.base.format(self.city)
        headers = {'User-Agent': self.ua.random}
        params = {'postal': self.zipcode, 'availabilityMode': '0'}
        proxies = {'http': self.proxy, 'https': self.proxy}

        if s:
            params['s'] = s

        resp = requests.get(
            url,
            headers=headers,
            params=params,
            proxies=proxies
        )

        retries = 0
        while resp.status_code != 200 and retries < 5:
            self.logger.info('Invalid response, retrying...')
            time.sleep(4)
            resp = requests.get(
                url,
                headers=headers,
                params=params,
                proxies=proxies
            )
            retries += 1

        search = {
            'content': resp.content,
            'headers': headers,
            'params': params,
            'proxies': proxies,
            'timestamp': datetime.datetime.utcnow(),
            'url': url
        }
        self._writesearchtomongo(search)
        return resp.content

    def _writelistingstomongo(self, listings):
        scraper_db = self.mongoclient.scraper
        listing_collection = scraper_db.listing
        for listing in listings:
            listing_collection.insert_one(listing)
        self.logger.info('Wrote {} listings to MongoDB'.format(
                len(listings)
            )
        )

    def _writesearchtomongo(self, search):
        scraper_db = self.mongoclient.scraper
        search_collection = scraper_db.search
        search_collection.insert_one(search)


if __name__ == '__main__':
    import sys

    from pymongo import MongoClient

    mongoclient = MongoClient('localhost', 27017)
    zipcodesearch = ZipCodeSearch(sys.argv[1], sys.argv[2], mongoclient)
    zipcodesearch.execute()
