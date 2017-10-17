'''rentscraper.scraper
'''
import sys

from rentscraper import zipcoderequest
from rentscraper import zipcodesearch
from rentscraper import listingscraper
from renscraper.log import get_configured_logger

def main(argv):
    if len(argv) < 3:
        raise ValueError('Must provide city and state')

    city = argv[1]
    state = argv[2]
    request = zipcoderequest.ZipCodeRequest(city, state)
    zipcodes = request.execute()
    for zipcode in zipcodes:
        search = zipcodesearch.ZipCodeSearch(city, zipcode)
        search.execute()
        logger.info('Compiled results for zip code {}'.format(zipcode)

        scraper = listingscraper.ListingScraper(zipcode)
        scraper.execute()
        logger.info('Gathered listings for zip code {}'.format(zipcode)

if __name__ == '__main__':
    main(sys.argv)
