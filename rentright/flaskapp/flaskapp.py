import pandas as pd
import pickle

from rentright.scrape.contentscraper import ContentScraper
from rentright.scrub.listing import Listing

from flask import Flask, render_template, request, json
from sklearn.ensemble import RandomForestRegressor


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def flaskapp():
    if request.method == 'POST':
        pass

    return render_template('index.html')

@app.route('/estimate', methods = ['POST'])
def estimate():
    link = request.form['link']

    # Make a request to retrieve page contents
    contentscraper = ContentScraper()
    content = contentscraper.executeOne(link)

    # Parse the listing to get all the attributes
    #   Set actual = 'price'
    listing = Listing(content, listing_id=None, zipcode=None)
    unit = listing.clean()
    actual_price = unit['price']

    print('actual_price: %s' % actual_price)

    attr_set = {'house', 'attached garage', 'duplex', 'cottage/cabin',
                'cats are OK - purrr', 'flat', 'street parking',
                'laundry on site', 'apartment', 'dogs are OK - wooof',
                'furnished', 'laundry in bldg', 'in-law', 'w/d in unit',
                'no smoking', 'townhouse', 'w/d hookups', 'no laundry on site',
                'manufactured', 'assisted living', 'condo',
                'carport', 'valet parking', 'land', 'wheelchair accessible',
                'no parking', 'off-street parking', 'detached garage'}

    feature_set = {'w/d in unit', 'price', 'sqft', 'cats are OK - purrr',
                   'latitude', 'detached garage', 'longitude', 'num_images',
                   'bedrooms', 'apartment', 'dogs are OK - wooof',
                   'no smoking', 'bathrooms'} | attr_set

    print('Set the sets')

    unit_features = {
        key: val for key, val in unit.data.items() if key in feature_set
    }
    empty_df = pd.DataFrame(columns=feature_set)
    unit_df = pd.DataFrame(unit_features, index=[0, ])
    df = pd.concat([unit_df, empty_df])
    df.fillna(False, inplace=True)

    print('Build the df')

    features = list(
        set(df.columns) - {'_id', 'description', 'listing_id', 'price', 'title'}
    )
    X = df[features]

    print('Got some features')

    # Feed all the attributes into the model to make one estimate
    #   Set estimate = 'estimate'
    rentrightmodel = pickle.load(open('/home/ubuntu/rent-right/rentright/data/rentrightmodel-v1.pkl', 'rb'))
    estimated_price = rentrightmodel.predict(X)

    print('estimated_price: %s' % estimated_price)

    model_pkl.close()

    # Return the estimate and actual price, which gets set on the client side
    return json.dumps({
        'status': 'OK',
        'estimate': estimated_price,
        'actual': actual_price
    })

if __name__ == '__main__':
    app.run()
