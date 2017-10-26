import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

from rentright.model.preprocessor import Preprocessor
from rentright.utils.mongo import get_mongoclient

def score(model, X, y):
    error = list(map(
        abs,
        cross_val_score(
            model, X, y, cv=5, scoring='neg_mean_absolute_error')
        )
    )
    r2 = list(cross_val_score(model, X, y))

    print('Scores: %s' % error)
    print('Mean: %s' % np.mean(error))
    print('Std:  %s' % np.std(error))
    print('R^2: %s' % r2)
    print('Mean: %s' % np.mean(r2))
    print('Std: %s' % np.std(r2))

def main():
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)

    X = preprocessor.getfeatures()
    y = preprocessor.getlabels()

    model = LinearRegression()
    score(model, X, y)

if __name__ == '__main__':
    main()
