'''rentscraper.search_for_listings
'''
import sys

from rentscraper.lib import zipcoderequest
from rentscraper.lib import zipcodesearch
from rentscraper.lib import listingscraper

def main(argv):
    '''
    '''
    if len(argv) < 3:
        raise ValueError('Must provide city and state')

    city = argv[1]
    state = argv[2]
    request = zipcoderequest.ZipCodeRequest(city, state)
    zipcodes = request.execute()
    for zipcode in zipcodes:
        search = zipcodesearch.ZipCodeSearch(zipcode)
        search.search()
        logger.info('Compiled results for zip code {}'.format(zipcode)

        scraper = listingscraper.ListingScraper(zipcode)
        scraper.scrape()
        logger.info('Gathered listings for zip code {}'.format(zipcode)
        
if __name__ == '__main__':
    main(sys.argv)
