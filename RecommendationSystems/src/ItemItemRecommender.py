
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

from time import time

import item_item_prototype as p


class ItemItemRecommender(object):
    def __init__(self, neighborhood_size):
        '''
        Initialize the parameters of the model.
        '''
        self.ratings_contents, self.ratings_as_mat = p.get_ratings_data()
        self.neighborhood_size=neighborhood_size
    def fit(self):
        '''
        Implement the model and fit it to the data passed as an argument.

        Store objects for describing model fit as class attributes.
        '''

        self.items_cos_sim, self.neighborhood=p.make_cos_sim_and_neighborhoods(self.ratings_mat, self.neighborhood_size)

    def _set_neighborhoods(self):
        '''
        Get the items most similar to each other item.

        Should set a class attribute with a matrix that is has
        number of rows equal to number of items and number of
        columns equal to neighborhood size. Entries of this matrix
        will be indexes of other items.

        You will call this in your fit method.
        '''
        pass

    def pred_one_user(self, user_id, timing =False) :
        '''
        Accept user id as arg. Return the predictions for a single user.

        Optional argument to specify whether or not timing should be provided
        on this operation.
        '''
        if timing:
            runtime= timeit
            user_1_preds= p.pred_one_user(self.items_cos_sim, self.neighborhood_size, self.ratings_as_mat, user_id)
        else:
            user_1_preds= p.pred_one_user(self.items_cos_sim, self.neighborhood_size, self.ratings_as_mat, user_id)
        return  runtime, user_1_preds

    def pred_all_users(self, timing =False):
        '''
        Repeated calls of pred_one_user, are combined into a single matrix.
        Return value is matrix of users (rows) items (columns) and predicted
        ratings (values).

        Optional argument to specify whether or not timing should be provided
        on this operation.
        '''
        n_users=self.ratings_mat.shape[0]
        n_items=self.ratings_mat.shape[1]
        runtime = np.zeros(n_users)

        output= np.zeros([n_users, n_items])

        for user in range(n_users):
            runtime = np.append(runtime, self.pred_one_user(user, timing=timing)[0])
            output[user]=self.pred_one_user(user, timing=timing)[1]

        return output



    def top_n_recs(self, user_id, n_top):
        '''
        Take user_id argument and number argument.

        Return that number of items with the highest predicted ratings, after
        removing items that user has already rated.
        '''
        output= self.pred_one_user(user_id)[1].nonzero()
        return output.argsort()[::-1][:n_top]
