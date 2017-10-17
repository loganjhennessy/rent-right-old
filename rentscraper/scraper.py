"""rentscraper.scraper"""
import sys

from log import get_configured_logger
from pymongo import MongoClient

from contentscraper import ContentScraper
from zipcoderequest import ZipCodeRequest
from zipcodesearch import ZipCodeSearch

def main(argv):
    """Main entry-point for scraper application.

    Arguments:
        argv: list of command line arguments

    argv must contain 3 arguments:
        [0]: standard, name of the file
        [1]: city
        [2]: state

    Raises:
        ValueError: Must provide both city and stats
    """
    if len(argv) != 3:
        raise ValueError('Must provide both city and state')

    city = argv[1]
    state = argv[2]

    mongoclient = MongoClient('localhost', 27017)

    zipcoderequest = ZipCodeRequest(city, state, mongoclient)
    zipcodes = zipcoderequest.execute()
    for zipcode in zipcodes:
        zipcodesearch = ZipCodeSearch(city, zipcode, mongoclient)
        zipcodesearch.execute()
        logger.info('Compiled results for zip code {}'.format(zipcode))

    for zipcode in zipcodes:
        contentscraper = ContentScraper(city, zipcode, mongoclient)
        contentscraper.execute()
        logger.info('Gathered listings for zip code {}'.format(zipcode)

if __name__ == '__main__':
    main(sys.argv)
