import numpy as np

from sklearn.model_selection import cross_val_score


class Evaluator(object):

    def __init__(self, model, X, y):
        self.model = model
        self.X = X
        self.y = y

        self.error = None
        self.r2 = None

    def evaluate(self):
        self.error = list(map(abs,
            cross_val_score(
                self.model,
                self.X,
                self.y,
                cv=5,
                scoring='neg_mean_absolute_error'
            )
        ))
        self.r2 = list(cross_val_score(self.model, self.X, self.y))

    def results(self):
        headers = ['Run', 'Error', 'R<sup>2</sup>']
        header = '|' + '|'.join(headers) + '|'
        align = '|:-:|--:|--:|'
        rows = ['|{}|{:6.2f}|{:6.2f}|'.format(
            i + 1,
            self.error,
            self.r2
        ) for i, (self.error, self.r2) in enumerate(zip(self.error, self.r2))]
        rows = '\n'.join(rows)
        mean = '|Mean|{:6.2f}|{:6.2f}|'.format(
            np.mean(self.error), np.mean(self.r2))
        std = '|Std|{:6.2f}|{:6.2f}|'.format(
            np.std(self.error), np.std(self.r2))
        return '\n'.join([header, align, rows, mean, std])