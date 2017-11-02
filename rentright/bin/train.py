import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor

from rentright.utils.mongo import get_mongoclient


def gettrainingdata():
    mongoclient = get_mongoclient()
    units = mongoclient.scraper.unit.find()
    units_list = list(units)
    df = pd.DataFrame(units_list)
    df.fillna(False, inplace=True)
    df = df[(df['price'] < 15000) & (df['price'] > 0) & (df['sqft'] != 0) & (df['sqft'] < 7500)]

    exclude_list = [
        '_id',
        'description',
        'listing_id',
        'price',
        'title',
        'zipcode'
    ]
    features = list(set(df.columns) - set(exclude_list))
    X = df[features]
    y = df['price']
    return X, y


def trainmodel(X, y):
    rfr = RandomForestRegressor(n_estimators=1000, criterion='mae', n_jobs=36, verbose=2)
    rfr.fit(X, y)
    return rfr


def savemodel(model):
    with open('/home/ubuntu/rent-right/rentright/data/rentrightmodel-v1.pkl', 'wb') as f:
        pickle.dump(model, f, protocol=-1)


def main():
    X, y = gettrainingdata()
    model = trainmodel(X, y)
    savemodel(model)


if __name__ == '__main__':
    main()
