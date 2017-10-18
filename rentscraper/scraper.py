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
        [3]: run option (search, scrape, or both)

    Raises:
        ValueError: Must provide city, state, and run option
    """
    if len(argv) != 4:
        raise ValueError('Must provide city, state, and ruun option')

    city = argv[1]
    state = argv[2]
    run_option = argv[3]

    zipcodes = get_zips(city, state)

    mongoclient = MongoClient('localhost', 27017)

    if run_option == 'search' or run_option == 'both':
        run_search(city, zipcodes, mongoclient)

    if run_option == 'scrape' or run_option == 'both':
        scrape_content(city, zipcodes, mongoclient)

def get_zips(city, state):
    """Get zip codes for the input city and state.

    Uses the Zip Code API at https://www.zipcodeapi.com. Requies ZIP_KEY
    environment variable set to your Zip Code API key. This can be obtained for
    free by registering on their website.

    Arguments:
        city: str, the city to search
        state: state, the state to search

    Returns:
        zipcodes: list of zipcodes for the input city and state
    """
    zipcoderequest = ZipCodeRequest(city, state)
    zipcodes = zipcoderequest.execute()
    return zipcodes

def run_search(city, zipcodes, mongoclient):
    """Run a search for listings in a specific zip code and write to mongoDB.

    City is required as well because it is part of the base URL for searching.

    Arguments:
        city: str, the city to use in the URL
        zipcode: str, the zipcode to search in for listings
        mongoclient: MongoClient object in which to write results
    """
    logger = get_configured_logger('DEBUG', __name__)
    for zipcode in zipcodes:
        zipcodesearch = ZipCodeSearch(city, zipcode, mongoclient)
        zipcodesearch.execute()
        logger.info('Compiled results for zip code {}'.format(zipcode))

def scrape_content(zipcodes, mongoclient):
    """Scrape listing content for a particular zip code and write to mongo.

    Arguments:
        zipcode: str, the zipcode to search in for listings
        mongoclient: MongoClient object in which to write results
    """
    logger = get_configured_logger('DEBUG', __name__)
    for zipcode in zipcodes:
        contentscraper = ContentScraper(zipcode, mongoclient)
        contentscraper.execute()
        logger.info('Gathered listings for zip code {}'.format(zipcode))

if __name__ == '__main__':
    main(sys.argv)
