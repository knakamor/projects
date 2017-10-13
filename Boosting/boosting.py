import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.base import clone
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble.partial_dependence import plot_partial_dependence
import matplotlib.pyplot as plt
import numpy as np




class AdaBoostBinaryClassifier(object):
    '''
    INPUT:
    - n_estimator (int)
      * The number of estimators to use in boosting
      * Default: 50

    - learning_rate (float)
      * Determines how fast the error would shrink
      * Lower learning rate means more accurate decision boundary,
        but slower to converge
      * Default: 1
    '''

    def __init__(self,
                 n_estimators=50,
                 learning_rate=1):

        self.base_estimator = DecisionTreeClassifier(max_depth=1)
        self.n_estimator = n_estimatorscf
        self.learning_rate = learning_rate

        # Will be filled-in in the fit() step
        self.estimators_ = []
        self.estimator_weight_ = np.zeros(self.n_estimator, dtype=np.float)
        #self.sign = np.ones(len(y), dtype=np.float)


    def fit(self, x, y):
        ''',
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels

        Build the estimators for the AdaBoost estimator.
        '''
        sample_weight= np.repeat(1/len(y), len(y))

        for i in range(self.n_estimator):
            self.estimators_.append(self._boost(x, y, sample_weight)[0])
            sample_weight=self._boost(x, y, sample_weight)[1]
            self.estimator_weight_[i]=self._boost(x, y, sample_weight)[2]



    def _boost(self, x, y, sample_weight):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels
        - sample_weight: numpy array

        OUTPUT:
        - estimator: DecisionTreeClassifier
        - sample_weight: numpy array (updated weights)
        - estimator_weight: float (weight of estimator)

        Go through one iteration of the AdaBoost algorithm. Build one estimator.
        '''


        estimator = clone(self.base_estimator)

        estimator.fit(x, y, sample_weight=sample_weight)

        estimator_error = np.dot(sample_weight, [y!= estimator.predict(x)]/np.sum(sample_weight)

        self.estimator_weight_= (1-estimator_error)/estimator_error 

        sample_weight= np.dot(self.sample_weight,  np.exp(self.estimator_weight * [y!= estimator.predict(x)]))

        estimator.fit(x,y, sample_weight=sample_weight)

        return estimator,  sample_weight,  self.estimator_weight_

    def predict(self, x):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix

        OUTPUT:
        - labels: numpy array of predictions (0 or 1)
        '''



        pred_y= [estimator.predict(x) for estimator in self.estimators_]

        def convert_y(y):
            return [-1 for i in y if i == 0 ]

        pred_y =convert_y(pred_y)

        return np.dot(pred_y, self.estimator_weight_)


    def score(self, x, y):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels

        OUTPUT:
        - score: float (accuracy score between 0 and 1)
        '''

        return 1.00 * sum(y[self.predict(x)==y])/len(y)
