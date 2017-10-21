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
    count = listings.count()
    logger.info('Cleaning {} listings.'.format(count))
    for i, listing in enumerate(listings):
        logger.info('Cleaning listing {} of {}.'.format(i, count))
        l = Listing(listing['content'], listing['_id'], listing['zipcode'])
        try:
            unit = l.clean()
            units.append(unit)
            logger.debug('Attributes: {}'.format(l.getattrs()))
            attrs.update(l.getattrs())
        except Exception as e:
            logger.warn('Caught exception while cleaning.')
            logger.warn('Listing URL: {}'.format(listing['link']))
            logger.warn(e)
            break

    return attrs, units

def findremoved(listings):
    """Get a list of the listings that have been removed.

    Arguments:
        listings: pymongo cursor with listings to check.

    Returns:
        removed: list of listings that have been removed.
    """
    logger = get_configured_logger('DEBUG', __name__)
    removed = []
    count = listings.count()
    for i, listing in enumerate(listings):
        logger.debug('Checking listing {} of {}.'.format(i, count))
        l = Listing(listing['content'], listing['_id'])
        if l.isremoved():
            logger.debug(
                    'Listing {} of {} not there anymore.'.format(i, count)
            )
            logger.debug(
                    'Adding {} to the removal list.'.format(listing['link'])
            )
            removed.append(listing)
        if not l.hasprice():
            removed.append(listing)
    return removed

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

def removelistings(mongoclient, removed):
    """Remove a list of listings from the database.

    Arguments:
        mongoclient: database client for the database containing the listings.
        remove: list of listing to remove
    """
    logger = get_configured_logger('DEBUG', __name__)
    logger.info('Removing {} listings.'.format(len(removed)))
    listing_collection = mongoclient.scraper.listing
    count = len(removed)
    for i, listing in enumerate(removed):
        logger.debug('  {} of {} removed from DB.'.format(i + 1, count))
        query = {"_id": listing['_id']}
        listing_collection.delete_one(query)

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

def main(argv):
    """Main entry-point for batchclean."""
    remove = False
    if argv[1] == 'remove':
        remove = True

    logger = get_configured_logger('DEBUG', __name__)

    mongoclient = MongoClient('localhost', 27017)
    logger.info('Retrieved mongoclient.')

    listings = queryforlistings(mongoclient)
    logger.info('Found {} listings.'.format(listings.count()))

    if remove:
        removed = findremoved(listings)
        logger.info(
            '{} listings have been removed, deleting from DB.'.format(len(removed))
        )
        removelistings(mongoclient, removed)

    listings = queryforlistings(mongoclient)
    attrs, units = cleanlistings(listings)
    logger.info(
        'Observed {} unique attributes while cleaning.'.format(len(attrs))
    )
    logger.info('Processed {} units'.format(len(units)))
    writeunitstomongo(mongoclient, units)
    writeattrstomongo(mongoclient, attrs)

if __name__ == '__main__':
    main(sys.argv)
