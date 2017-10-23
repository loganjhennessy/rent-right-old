from pymongo import MongoClient

def main():
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PASS = os.environ['MONGO_PASS']
    MONGO_IP = os.environ['MONGO_IP']
    connstr = 'mongodb://{}:{}@{}/scraper'
    mongoclient = MongoClient(connstr.format(MONGO_USER, MONGO_PASS, MONGO_IP))
	listing_collection = client.scraper.listing
    listings = listing_collection.find()
    for listing in listings:
        query = {'_id': listing['_id']}
        update = {'$set': {'content_parsed': False}}
        listing_collection.update_one(query, update)

    unit_collection = client.scraper.unit
    unit_collection.drop()

if __name__ == '__main__':
    main()
