import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor

from rentright.utils.mongo import get_mongoclient


def gettrainingdata():
    mongoclient = get_mongoclient()
    units = mongoclient.scraper.unit.find()
    df = pd.DataFrame(units)
    df = df[(df['price'] < 25000) & (df['sqft'] != 0) & (df['sqft'] < 10000)]

    exclude_list = ['_id', 'description', 'listing_id', 'price', 'title']
    features = list(set(df.columns) - set(exclude_list))
    X = df[features]
    y = df['price']
    return X, y


def trainmodel(X, y):
    rfr = RandomForestRegressor(max_depth=100000, criterion='mae')
    rfr.fit(X, y)
    return rfr


def savemodel(model):
    with open('../data/rentrightmodel.pkl', 'wb') as f:
        pickle.dump(model, f)


def main():
    X, y = gettrainingdata()
    model = trainmodel(X, y)
    savemodel(model)


if __name__ == '__main__':
    main()