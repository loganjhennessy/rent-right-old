"""rentscraper.batchclean"""
import sys

from log import get_configured_logger
from pymongo import MongoClient

from listing import Listing

def cleanlistings(listings):
    """Clean a list of listings and return a clean unit object.

    Arguments:
        listings: pymongo cursor containing all listings

    Returns:
        attrs: set of boolean attributes found in all the listings
        units: list of Unit objects representing the cleaned listings
    """
    logger = get_configured_logger('DEBUG', __name__)
    units = []
    attrs = set()
    for listing in listings:
        l = Listing(listing['content'], listing['_id'])
        
        try:
            unit = l.clean()
            units.append(unit)
            attrs.update(l.getattrs())
        except Exception as e:
            logger.info('Caught exception while cleaning.')
            logger.info('Listing URL: {}'.format(listing['link']))
            logger.info(e)
            break

    return attrs, units

def queryforlistings(mongoclient):
    """Get all listings in the mongo database

    Arguments:
        mongoclient: mongo db to get listings from

    Returns:
        listings: list
    """
    listing_collection = mongoclient.scraper.listing
    query = {"content_parsed": False, "content_acquired": True}
    listings = listing_collection.find(query)
    return listings

def writeattrstomongo(mongoclient, attrs):
    """Write a set of attributes to mongo database.

    Arguments:
        attrs: a set of attributes to write to mongo
    """
    attr_collection = mongoclient.scraper.attr
    for attr in attrs:
        if not attr_collection.find_one({"attr": attr}):
            attr_collection.insert_one({"attr": attr})

def writeunitstomongo(mongoclient, units):
    """Write unit objects to mongo database.

    Arguments:
        mongoclient: mongo db to write to
    """
    unit_collection = mongoclient.scraper.unit
    listing_collection = mongoclient.scraper.listing
    for unit in units:
        unit_collection.insert_one(dict(unit))
        query = {"_id": unit['listing_id']}
        update = {"$set": {"content_parsed": True}}
        listing_collection.update_one(query, update)

def main():
    """Main entry-point for batchclean."""
    logger = get_configured_logger('DEBUG', __name__)

    mongoclient = MongoClient('localhost', 27017)
    logger.info('Retrieved mongoclient.')

    listings = queryforlistings(mongoclient)
    logger.info('Found {} listings.'.format(listings.count()))

    attrs, units = cleanlistings(listings)
    logger.info('Observed {} unique attributes while cleanin.'.format(len(attrs)))
    logger.info('Processed {} units'.format(len(units)))
    writeunitstomongo(mongoclient, units)
    writeattrstomongo(mongoclient, attrs)

if __name__ == '__main__':
    main()
