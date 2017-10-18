"""rentscraper.contentscraper"""
import datetime
import os
import requests
import time

from fake_useragent import UserAgent
from log import get_configured_logger
from requests.exceptions import ProxyError, SSLError
from requests.packages.urllib3.exceptions import MaxRetryError

class ContentScraper(object):
    """Implements a content scrape for a list of listings.

    Assumes that listings have been stored in MongoDB.

    Attributes:
        logger: self explanatory
        monogoclient: MongoClient object for writing results
        proxy: proxy IP set by env var HTTP_PROXY
        ua: UserAgent object to generate random user agents
        zipcode: zip code for this scrape
    """

    def __init__(self, zipcode, mongoclient):
        """Init ContentScraper with zipcode and mongoclient.

        proxy is set to value of HTTP_PROXY environment variable
        logger is retrieved from get_configured_logger function
        """
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
        """Executes a content scrape for the requested zip code."""
        listings = self._query_listings()

        self.logger.info(
            'Found {} new listings for this zip code'.format(
                listings.count()
            )
        )

        for listing in listings:
            time.sleep(1)
            url = listing['link']
            self.logger.info('Scraping details for: {}'.format(url))
            content = self._scrape_details(url)
            self.logger.info('Writing to mongo')
            self._writedetailstomongo(url, content, listing)

    def _query_listings(self):
        """Get a list of listings to scrape.

        Filtered using the 'content_acquired' column in the listing table so
        that only listings that have not had content acquired will be returned.

        Returns:
            list of listings to get content from
        """
        scraper_db = self.mongoclient.scraper
        listings = scraper_db.listing.find({
            "zipcode": self.zipcode,
            "content_acquired": False
        })
        return listings

    def _scrape_details(self, url):
        """Get a page of content.

        Configures user-agent header and http(s) proxy to make a safe scrape
        of a particular URL.

        Arguments:
            url: str, the url to get the content from

        Returns:
            str containing content from the url
        """
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

    def _writedetailstomongo(self, url, content, listing):
        """Write the results of a scrape to MongoDB.

        The original listing object is passed through so that the record in the
        table can be updated to reflect that the content has been acquired.

        Arguments:
            url: the url that was scraped
            content: the content from  that url
            listing: the original listing
        """
        scraper_db = self.mongoclient.scraper
        query = {"_id": listing['_id']}
        listing_collection = scraper_db.listing
        listing_collection.update_one(
            {"_id": listing['_id']},
            {"$set": {
                "content": content,
                "content_acquired": True,
                "time_content_acquired": datetime.datetime.utcnow()
            }}
        )

if __name__ == '__main__':
    import sys

    from pymongo import MongoClient
    mongoclient = MongoClient('localhost', 27017)
    listingscraper = ListingScraper(sys.argv[1], mongoclient)
    listingscraper.execute()
