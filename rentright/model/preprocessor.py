"""rentright.model.preprocessor"""
import pandas as pd

from rentright.utils.mongo import get_mongoclient


class Preprocessor(object):
    """Preprocesses data for training the rentright model."""
    def __init__(self,
                 mongoclient,
                 maxprice=15000,
                 maxsqft=7500,
                 zipcode=None):
        self.df = None # set by process() method
        self.mongoclient = mongoclient
        self.maxprice = maxprice
        self.maxsqft = maxsqft
        self.units = self.mongoclient.scraper.unit.find()
        self.zipcode = zipcode

    def getfeatures(self):
        self._makedataframe()
        self._applyfilters()
        #self._makefeatures()
        excludelist = ['_id', 'description', 'listing_id', 'price', 'title', 'zipcode']
        features = list(set(self.df.columns) - set(excludelist))

        X = self.df[features]
        return X

    def getlabels(self):
        y = self.df['price']
        return y

    def _applyfilters(self):
        self.df = self.df[
            (self.df['price'] < self.maxprice) &
            (self.df['price'] > 0) &
            (self.df['sqft'] != 0) &
            (self.df['sqft'] < self.maxsqft)
        ]
        if self.zipcode:
            self.df = self.df[self.df['zipcode'] == self.zipcode]

    def _makedataframe(self):
        df = pd.DataFrame(list(self.units))
        df.fillna(False, inplace=True)
        self.df = df

    def _makefeatures(self):
        transforms = [
            textstate.flesch_kincaid_grade
        ]

        # apply transforms
        transformsdf = self.df.transform(transforms)

        # join the results
        self.df.join(transformsdf)



if __name__ == '__main__':
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)
    preprocessor.makedataframe()
