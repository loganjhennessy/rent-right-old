import pandas as pd
import pickle

from rentright.scrape.contentscraper import ContentScraper
from rentright.scrub.listing import Listing

from flask import Flask, render_template, request, json

application = Flask(
    __name__, 
    template_folder='/home/ubuntu/rent-right/rentright/flaskapp/templates'
)


@application.route('/', methods = ['POST', 'GET'])
def flaskapp():
    if request.method == 'POST':
        pass

    return render_template(
            'index.html'
    )


@application.route('/estimate', methods = ['POST'])
def estimate():
    link = request.form['link']

    # Make a request to retrieve page contents
    contentscraper = ContentScraper()
    content = contentscraper.executeOne(link)

    # Parse the listing to get all the attributes
    listing = Listing(content, listing_id=None, zipcode=None)
    unit = listing.clean()
    actual_price = unit['price']

    feature_set = {'bedrooms', 'bathrooms', 'sqft', 'latitude', 'longitude', 'pets'}

    unit_features = {
        key: val for key, val in unit.data.items() if key in feature_set
    }
    empty_df = pd.DataFrame(columns=feature_set)
    unit_df = pd.DataFrame(unit_features, index=[0, ])
    df = pd.concat([unit_df, empty_df])
    df.fillna(False, inplace=True)

    df['pets'] = df['cats are OK - purrr'] | df['dogs are OK - wooof']
    features = list(feature_set)
    X = df[features]

    # Feed all the attributes into the model to make one estimate
    estimated_price = rentrightmodel.predict(X)

    print('actual_price: %s' % actual_price)
    print('estimated_price: %s' % estimated_price[0])

    # Return the estimate and actual price, which gets set on the client side
    return json.dumps({
        'status': 'OK',
        'estimate': str(estimated_price[0]),
        'actual': str(actual_price)
    })


if __name__ == '__main__':
    with open('/home/ubuntu/rent-right/rentright/flaskapp/data/rent-right-model-v2.pkl', 'rb') as f:
        rentrightmodel = pickle.load(f, encoding='bytes')
    application.run()

