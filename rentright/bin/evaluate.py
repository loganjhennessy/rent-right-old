import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

from rentright.model.evaluator import Evaluator
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
    printtable(error, r2)

def printtable(error, r2):
    headers = ['Run', 'Error', 'R<sup>2</sup>']
    header = '|' + '|'.join(headers) + '|'
    align = '|:-:|--:|--:|'
    rows = ['|{}|{:6.2f}|{:6.2f}|'.format(i + 1, error, r2) for i, (error, r2) in enumerate(zip(error, r2))]
    rows = '\n'.join(rows)
    mean = '|Mean|{:6.2f}|{:6.2f}|'.format(np.mean(error), np.mean(r2))
    std = '|Std|{:6.2f}|{:6.2f}|'.format(np.std(error), np.std(r2))
    return '\n'.join([header, align, rows, mean, std])

def main():
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)

    X = preprocessor.getfeatures()
    y = preprocessor.getlabels()

    model = LinearRegression()
    evaluator = Evaluator(model, X, y)
    evaluator.evaluate()
    print('Ran on {} units...'.format(X.shape[0]))
    print(evaluator.results())

if __name__ == '__main__':
    main()
