"""rentright.scraper.contentscraper"""
import datetime
import os
import requests
import time

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, SSLError
from requests.packages.urllib3.exceptions import MaxRetryError

from rentright.utils.log import get_configured_logger

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
        self.sleeplong = 2
        self.sleepshort = 0.5
        self.ua = UserAgent()
        self.zipcode = zipcode

        self.logger.info(
            'ListingScraper initialized for zip code {}'.format(self.zipcode)
        )

    def execute(self):
        """Executes a content scrape for the requested zip code."""
        listings = self._query_listings()

        self.logger.info(
            'Found {} new listings for this zip code'.format(listings.count())
        )

        total_listings = listings.count()

        for i, listing in enumerate(listings):
            #time.sleep(self.sleepshort)
            url = listing['link']
            self.logger.info('Scraping details for: {}'.format(url))
            content = self._scrape_details(url)
            self._writedetailstomongo(url, content, listing)
            self.logger.info('Listing {} of {} written to MongoDB.'.format(
                i + 1, total_listings
            ))

    def _postnotfound(self, content):
        """Returns whether or not the page has a .post-not-found-heading

        Arguments:
            content: str of content

        Returns:
            bool: True if content has .post-not-found-heading class
        """
        soup = BeautifulSoup(content, 'html.parser')
        if soup.select('.post-not-found-heading'):
            return True
        else:
            return False

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
        }, no_cursor_timeout=True)
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

        while True:
            try:
                resp = requests.get(url, headers=headers, proxies=proxies)
                if self._postnotfound(resp.content):
                    self.logger.info('Page not found.')
                    break
                if resp.status_code != 200:
                    raise Exception(
                            'Response contained invalid '
                            'status code {}'.format(resp.status_code)
                          )
                break
            except Exception as e:
                self.logger.info('Exception occurred during request.')
                self.logger.info('{}'.format(e))
                self.logger.info(
                    'Sleeping for {} seconds'.format(self.sleeplong)
                )
                time.sleep(self.sleeplong)
                self.logger.info('Retrying')

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
                "content_parsed": False,
                "time_content_acquired": datetime.datetime.utcnow()
            }}
        )

if __name__ == '__main__':
    import sys

    from pymongo import MongoClient
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PASS = os.environ['MONGO_PASS']
    MONGO_IP = os.environ['MONGO_IP']
    connstr = 'mongodb://{}:{}@{}/scraper'
    mongoclient = MongoClient(connstr.format(MONGO_USER, MONGO_PASS, MONGO_IP))
    listingscraper = ListingScraper(sys.argv[1], mongoclient)
    listingscraper.execute()
