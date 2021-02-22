import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.base import BaseEstimator, TransformerMixin


class GPSDBSCAN(BaseEstimator, TransformerMixin):
    """
        Detects if vehicle moving too fast for waste collection.
    """
    def __init__(self, eps: int, min_n_samples: int,
                 cols2select: list, fast_movement_col: str,
                 cluster_colname: str, post_sort_cols: list):
        """
            Arguments:
                * eps (int): Max distance between observation
                * min_n_samples (int): Minimum samples count to form clusters
                * cols2select (list<str>): List of column names
                                           to be used by model
                * fast_movement_col (str): Column name with fast movement mark
                * cluster_colname (str): Column name cluster id will assigned
                * post_sort_cols (list<str>): Column names to perform sort
                                              after fast movement splitting
        """
        self.eps = eps
        self.min_n_samples = min_n_samples
        self.cols2select = cols2select
        self.fast_movement_col = fast_movement_col
        self.cluster_colname = cluster_colname
        self.post_sort_cols = post_sort_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        # 1. Select slow moving records

        X_slow_moving_points = X[~X[self.fast_movement_col]]
        X_fast_moving_points = X[X[self.fast_movement_col]]

        # 1. Model init
        model = DBSCAN(eps=self.eps, min_samples=self.min_n_samples)

        # 2. Predict
        DBSCAN_X = X_slow_moving_points[self.cols2select]
        X_slow_moving_points.loc[:, self.cluster_colname] = \
            model.fit_predict(DBSCAN_X)

        # 3. Back concatenation & fillna
        X = pd.concat([
            X_slow_moving_points,
            X_fast_moving_points,
        ])
        X[self.cluster_colname] = X[self.cluster_colname].fillna(-1)

        # 4. Post sorting
        X = X.sort_values(by=self.post_sort_cols).reset_index(drop=True)

        return X
