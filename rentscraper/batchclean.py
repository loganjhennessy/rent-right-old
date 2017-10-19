"""rentscraper.batchclean"""
import sys

from log import get_configured_logger
from pymongo import MongoClient

from listing import Listing

from absl import app

def cleanlistings(listings):
    """Clean a list of listings and return a clean unit object.

    Arguments:
        listings: pymongo cursor containing all listings

    Returns:
        attrs: set of boolean attributes found in all the listings
        units: list of Unit objects representing the cleaned listings
    """
    units = []
    attrs = set()
    for listing in listings:
        l = Listing(listing['content'])
        unit = l.clean()
        units.append(unit)
        attrs.update(l.getattrs())

    return attrs, units

def queryforlistings(mongoclient):
    """Get all listings in the mongo database

    Arguments:
        mongoclient: mongo db to get listings from

    Returns:
        listings: list
    """
    listing_collection = mongoclient.scraper.listing
    query = {"content_parsed": False}
    listings = listing_collection.find(query)
    return listings

def writeattrstomongo(mongoclient, attrs):
    """Write a set of attributes to mongo database.

    Arguments:
        attrs: a set of attributes to write to mongo
    """
    attr_collection = mongoclient.scraper.attr
    for attr in attrs:
        if not attr_collection.find_one({"attr": attr})
            attr_collection.insert_one({"attr": attr})

def writeunitstomongo(mongoclient, units):
    """Write unit objects to mongo database.

    Arguments:
        mongoclient: mongo db to write to
    """
    unit_collection = mongoclient.scraper.unit
    listing_collection = mongoclient.scraper.listing
    for unit in units
        unit_collection.insert_one(dict(unit))
        query = {"_id": unit['listing_id']}
        update = {"$set": {"content_parsed": True}}
        listing_collection.update_one(query, update)

def main(argv):
    """Main entry-point for batchclean."""
    del argv # unused

    mongoclient = MongoClient('localhost', 27017)
    listings = queryforlistings(mongoclient)
    attrs, units = cleanlistings(listings)
    writeunitstomongo(mongoclient, units)
    writeattrstomongo(mongoclient, attrs)

if __name__ == '__main__':
    app.run(main)
