"""rentright.bin.resetclean"""
from rentright.utils.mongo import get_mongoclient

def main():
    mongoclient = get_mongoclient()
    listing_collection = mongoclient.scraper.listing
    listings = listing_collection.find()
    for listing in listings:
        query = {'_id': listing['_id']}
        update = {'$set': {'content_parsed': False}}
        listing_collection.update_one(query, update)

    unit_collection = mongoclient.scraper.unit
    unit_collection.drop()

if __name__ == '__main__':
    main()
