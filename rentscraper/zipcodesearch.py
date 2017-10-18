"""rentscraper.zipcodesearch"""
import datetime
import os
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from log import get_configured_logger

class ZipCodeSearch(object):
    """Implements a search for all rental listings by zip code.

    Attributes:
        base: base URL for the search
        city: used to complete the base URL
        logger: self explanatory
        mongoclient: MongoClient object for writing results
        proxy: proxy IP set by env var HTTP_PROXY
        ua: UserAgent object to generate random user agents
        zipcode: zip code for this search
    """

    def __init__(self, city, zipcode, mongoclient):
        """Init ZipCodeSearch object with city, zipcode, and mongoclient.

        base is set to value of BASE_URL environment variable
        proxy is set to value of HTTP_PROXY environment variable
        logger is retrieved from get_configured_logger function
        """
        self.base = os.environ['BASE_URL']
        self.city = city.lower()
        self.logger = get_configured_logger('DEBUG', __name__)
        self.mongoclient = mongoclient
        self.proxy = os.environ['HTTP_PROXY']
        self.sleeplong = 10
        self.sleepshort = 1
        self.ua = UserAgent()
        self.zipcode = zipcode

        self.logger.info(
            'ZipCodeSearch initialized for zip code {}'.format(
                self.zipcode
            )
        )

    def execute(self):
        """Executes a zip code search for rental properties."""
        results = []
        content = self._search()
        results.append(content)
        count = self._countresults(content)
        self.logger.info(
            'Found {} results for this zip code'.format(count)
        )
        
        if count > 0:
            listings = self._parseresults(content)
            self._writelistingstomongo(listings)

        for s in range(120, int(count), 120):
            time.sleep(self.sleepshort)
            content = self._search(str(s))
            listings = self._parseresults(content, str(s))
            self._writelistingstomongo(listings)

    def _countresults(self, content):
        """Return number of results found in content.

        Arguments:
            content: str containing the contents of a search query response

        Returns:
            int: count of listings found in search
        """
        soup = BeautifulSoup(content, 'html.parser')

        count = 0
        if soup.select('.totalcount'):
            count = soup.select('.totalcount')[0].text
        return count

    def _parseresults(self, content, s='0'):
        """Parse results of a search for link and title.

        Arguments:
            content: str containing the contents of a search query response
            s: str, the current 'page' of serch results, defaults to '0'

        Returns:
            list of dicts representing parsed listings
        """
        listings = []
        soup = BeautifulSoup(content, 'html.parser')
        resulttitles = soup.select('.result-title.hdrlnk')
        for title in resulttitles:
            listing = {
                'content_acquired': False,
                'imgs_acquired': False,
                'link': title.attrs['href'],
                's': s,
                'time_added': datetime.datetime.utcnow(),
                'title': title.text,
                'zipcode': self.zipcode
            }
            listings.append(listing)
        self.logger.info('Parsed {} listings'.format(len(listings)))
        return listings

    def _search(self, s=None):
        """Get a page of search results.

        Includes re-try logic in case of bad proxy.

        Arguments:
            s: str, the search result index to start at, defaults to None

        Returns:
            str: content of the HTTP response
        """
        url = self.base.format(self.city)
        headers = {'User-Agent': self.ua.random}
        params = {'postal': self.zipcode, 'availabilityMode': '0'}
        proxies = {'http': self.proxy, 'https': self.proxy}

        if s:
            params['s'] = s

        while True:
            try:
                resp = requests.get(
                        url, 
                        headers=headers, 
                        params=params, 
                        proxies=proxies
                       )
                if resp.status_code != 200:
                    raise Exception(
                            'Response contained invalid '
                            'status code {}'.format(resp.status_code))
                break
            except Exception as e:
                self.logger.info('Exception occurred during request.')
                self.logger.info('{}'.format(e))
                self.logger.info('Sleeping for {} seconds'.format(self.sleeplong))
                time.sleep(self.sleeplong)
                self.logger.info('Retrying')

        

#        try:
#            resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#        except ProxyError:
#            self.logger.info('Caught ProxyError, retrying...')
#            time.sleep(10)
#            resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#        except SSLError:
#            self.logger.info('Caught SSLError, retrying...')
#            time.sleep(10)
#            resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#        except MaxRetryError:
#            self.logger.info('Caught MaxRetryError, retrying...')
#            time.sleep(10)
#            resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#
#        retries = 0
#        while resp.status_code != 200 and retries < 5:
#            self.logger.info('Invalid response, retrying...')
#            time.sleep(10)
#            try:
#                resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#            except ProxyError:
#                self.logger.info('Caught ProxyError, retrying...')
#                time.sleep(10)
#                resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#            except SSLError:
#                self.logger.info('Caught SSLError, retrying...')
#                time.sleep(10)
#                resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#            except MaxRetryError:
#                self.logger.info('Caught MaxRetryError, retrying...')
#                time.sleep(10)
#                resp = requests.get(url,headers=headers,params=params,proxies=proxies)
#            retries += 1

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
        """Write a list of listing dicts to mongoDB.

        Data is written to the 'scraper' database in a collection named
        'listings'.

        Arguments:
            listings: list of dicts containing listings
        """
        scraper_db = self.mongoclient.scraper
        listing_collection = scraper_db.listing
        for listing in listings:
            listing_collection.insert_one(listing)
        self.logger.info('Wrote {} listings to MongoDB'.format(
                len(listings)
            )
        )

    def _writesearchtomongo(self, search):
        """Write the results of a serach to mongoDB.

        Data is written to the 'scraper' database in a collection named
        'search'.

        Arguments:
            search: dict containing meta-information about a search.
        """
        scraper_db = self.mongoclient.scraper
        search_collection = scraper_db.search
        search_collection.insert_one(search)


if __name__ == '__main__':
    import sys

    from pymongo import MongoClient

    mongoclient = MongoClient('localhost', 27017)
    zipcodesearch = ZipCodeSearch(sys.argv[1], sys.argv[2], mongoclient)
    zipcodesearch.execute()
