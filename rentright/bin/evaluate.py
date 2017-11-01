from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from rentright.model.evaluator import Evaluator
from rentright.model.preprocessor import Preprocessor
from rentright.utils.mongo import get_mongoclient

def main():
    mongoclient = get_mongoclient()
    preprocessor = Preprocessor(mongoclient)

    X = preprocessor.getfeatures()
    y = preprocessor.getlabels()

    model = RandomForestRegressor(n_estimators=10000, criterion='mae', n_jobs=-1)
    evaluator = Evaluator(model, X, y)
    evaluator.evaluate()
    print('Ran on {} units...'.format(X.shape[0]))
    print(evaluator.results())

if __name__ == '__main__':
    main()
