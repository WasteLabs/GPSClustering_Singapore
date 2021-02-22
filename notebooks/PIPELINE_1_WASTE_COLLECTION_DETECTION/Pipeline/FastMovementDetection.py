import pickle
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from GPSOdyssey import Polaris


class FastMovementPreprocessor(TransformerMixin):

    def __init__(self, select_columns, datetime_column,
                 vehicle_id_col, lon_col, lat_col, n_parallel=4):
        self.select_columns = select_columns
        self.datetime_column = datetime_column
        self.vehicle_id_col = vehicle_id_col
        self.lon_col = lon_col
        self.lat_col = lat_col
        self.n_parallel = n_parallel

    def fit(self, X, y=None):
        return self

    def compute_velocity(self, X: pd.DataFrame) -> pd.DataFrame:
        X = Polaris(X) \
            .proj_coordinates(lon_in=self.lon_col, lat_in=self.lat_col,
                              lon_out='x', lat_out='y') \
            .add_velocity(x_col='x', y_col='y', unixtime_col='unixtime',
                          new_velocity_col='velocity', fillna=False) \
            .pandas_df_operation(func_name='fillna',
                                 columns=['velocity'],
                                 arguments={'method': 'ffill'}) \
            .add_lag_of_column('velocity', lag_shifts=[1, 2, 3, 4, 5]) \
            .pandas_df_operation(func_name='fillna',
                                 columns=['velocity_lag_1', 'velocity_lag_2',
                                          'velocity_lag_3', 'velocity_lag_4',
                                          'velocity_lag_5'],
                                 arguments={'method': 'bfill'}).df

        return X

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = Polaris(X) \
            .restore_mismatched_lon_lat(src_lon='lon', src_lat='lat',
                                        trgt_lon='lon_match',
                                        trgt_lat='lat_match') \
            .select_columns(self.select_columns) \
            .construct_datetime(datetime=self.datetime_column,
                                time_col='datetime') \
            .add_date_col('datetime', 'date') \
            .add_time_col('datetime', 'time') \
            .add_unixtime('datetime', 'unixtime').df

        # 2. Compute velocity column
        X = self.compute_velocity(X)
        return X


class FastMovementClassifier(BaseEstimator, TransformerMixin):
    """
        Detects if vehicle moving too fast for waste collection.
    """
    def __init__(self, model_path: str, X_cols: list, y_col: str):
        self.X_cols = X_cols
        self.y_col = y_col
        self.model = pickle.load(open(model_path, 'rb'))

    def fit(self, X, y=None):
        return self

    def remove_redundant_cols(self, X):
        cols2left = list(set(X.columns) - set(self.X_cols))
        return X[cols2left]

    def transform(self, X):

        # 1. Prediction
        X[self.y_col] = self.model.predict(X[self.X_cols])

        # 2. Remove redundant columns
        X = self.remove_redundant_cols(X)
        return X
