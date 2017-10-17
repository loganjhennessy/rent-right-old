import datetime
import os
import requests
import time

from fake_useragent import UserAgent
from log import get_configured_logger
from requests.exceptions import ProxyError, SSLError
from requests.packages.urllib3.exceptions import MaxRetryError

class ListingScraper(object):

    def __init__(self, zipcode, mongoclient):
        self.logger = get_configured_logger('DEBUG', __name__)
        self.mongoclient = mongoclient
        self.proxy = os.environ['HTTP_PROXY']
        self.ua = UserAgent()
        self.zipcode = zipcode

        self.logger.info(
            'ListingScraper initialized for zip code {}'.format(
                self.zipcode
            )
        )

    def execute(self):
        listings = self._query_listings()

        self.logger.info(
            'Found {} listings for this zip code'.format(
                listings.count()
            )
        )

        for listing in listings:
            time.sleep(1)
            url = listing['link']
            self.logger.info('Scraping details for: {}'.format(url))
            content = self._scrape_details(url)
            self.logger.info('Writing to mongo')
            self._writedetailstomongo(url, content)

    def _query_listings(self):
        scraper_db = self.mongoclient.scraper
        listings = scraper_db.listing.find({ "zipcode": self.zipcode })
        return listings

    def _scrape_details(self, url):
        headers = {'User-Agent': self.ua.random}
        proxies = {'http': self.proxy, 'https': self.proxy}

        try:
            resp = requests.get(url, headers=headers, proxies=proxies)
        except ProxyError:
            self.logger.info('Caught ProxyError, retrying...')
            time.sleep(4)
            resp = requests.get(url, headers=headers, proxies=proxies)
        except SSLError:
            self.logger.info('Caught SSLError, retrying...')
            time.sleep(4)
            resp = requests.get(url, headers=headers, proxies=proxies)
        except MaxRetryError:
            self.logger.info('Caught SSLError, retrying...')
            time.sleep(4)
            resp = requests.get(url, headers=headers, proxies=proxies)

        retries = 0
        while resp.status_code != 200 and retries < 5:
            self.logger.info('Invalid response, retrying...')
            time.sleep(4)
            try:
                resp = requests.get(url, headers=headers, proxies=proxies)
            except ProxyError:
                self.logger.info('Caught ProxyError, retrying...')
                time.sleep(4)
                resp = requests.get(url, headers=headers, proxies=proxies)
            except SSLError:
                self.logger.info('Caught SSLError, retrying...')
                time.sleep(4)
                resp = requests.get(url, headers=headers, proxies=proxies)
            except MaxRetryError:
                self.logger.info('Caught SSLError, retrying...')
                time.sleep(4)
                resp = requests.get(url, headers=headers, proxies=proxies)

            retries += 1

        return resp.content

    def _writedetailstomongo(self, url, content):
        scraper_db = self.mongoclient.scraper
        detail = {
            'content': content,
            'timestamp': datetime.datetime.utcnow(),
            'link': url,
            'zipcode': self.zipcode
        }

if __name__ == '__main__':
    import sys

    from pymongo import MongoClient
    mongoclient = MongoClient('localhost', 27017)
    listingscraper = ListingScraper(sys.argv[1], mongoclient)
    listingscraper.execute()
