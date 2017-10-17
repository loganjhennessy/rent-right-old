'''rentscraper.scraper
'''
import sys

from log import get_configured_logger
from pymongo import MongoClient

from listingscraper import ListingScraper
from zipcoderequest import ZipCodeRequest
from zipcodesearch import ZipCodeSearch

def main(argv):
    if len(argv) < 3:
        raise ValueError('Must provide city and state')

    city = argv[1]
    state = argv[2]

    mongoclient = MongoClient('localhost', 27017)

    zipcoderequest = ZipCodeRequest(city, state, mongoclient)
    zipcodes = zipcoderequest.execute()
    for zipcode in zipcodes:
        zipcodesearch = ZipCodeSearch(city, zipcode, mongoclient)
        zipcodesearch.execute()
        logger.info('Compiled results for zip code {}'.format(zipcode))

        listingscraper = ListingScraper(city, zipcode, mongoclient)
        listingscraper.execute()
        logger.info('Gathered listings for zip code {}'.format(zipcode)

if __name__ == '__main__':
    main(sys.argv)
