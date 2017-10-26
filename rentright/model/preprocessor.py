"""rentright.model.preprocessor"""
import pandas as pd

from rentright.utils.mongo import get_mongoclient

class Preprocessor(object):
    """Preprocesses data for training the rentright model."""
    def __init__(self, mongoclient):
        self.df = None # set by process() method
        self.mongoclient = mongoclient
        self.maxprice
        self.maxsqft
        self.units = self.mongoclient.scraper.unit.find()

    def getfeatures(self, features=None):
        if self.df == None and features == None:
            self.process()
            features = list(self.df.columns).remove('_id')

        X = self.df[features]
        return X

    def getlabels(self):
        y = self.df['price']
        return y

    def process(self):
        df = pd.DataFrame(list(self.units))
        df.fillna(False, inplace=True)
        df = df[
            (df['price'] < self.maxprice) &
            (df['sqft'] != 0) &
            (df['sqft'] < self.maxsqft)
        ]
        self.df = df
        return df

if __name__ == '__main__':
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)
    preprocessor.process()
