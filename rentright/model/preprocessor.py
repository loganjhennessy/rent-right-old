"""rentright.model.preprocessor"""
import pandas as pd

from rentright.utils.mongo import get_mongoclient


class Preprocessor(object):
    """Preprocesses data for training the rentright model."""
    def __init__(self,
                 mongoclient,
                 maxprice=25000,
                 maxsqft=10000,
                 zipcode=None):
        self.df = None # set by process() method
        self.mongoclient = mongoclient
        self.maxprice = maxprice
        self.maxsqft = maxsqft
        self.units = self.mongoclient.scraper.unit.find()
        self.zipcode = zipcode

    def getfeatures(self):
        if self.df == None:
            excludelist = ['_id', 'description', 'listing_id', 'price', 'title']
            features = list(set(self.df.columns) - set(excludelist))
            self.makedataframe()

        X = self.df[features]
        return X

    def getlabels(self):
        y = self.df['price']
        return y

    def makedataframe(self):
        df = pd.DataFrame(list(self.units))
        df.fillna(False, inplace=True)
        df = df[
            (df['price'] < self.maxprice) &
            (df['sqft'] != 0) &
            (df['sqft'] < self.maxsqft)
        ]

        if self.zipcode:
            df = df[df['zipcode'] == self.zipcode]

        self.df = df
        return df


if __name__ == '__main__':
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)
    preprocessor.makedataframe()
