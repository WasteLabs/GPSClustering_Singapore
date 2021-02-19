"""
    date: 27.11.2020
    Author: Adil Rashitov
"""
import numpy as np
import pandas as pd
import geopandas as gpd
# import os
# import json
# import pickle
# import lightgbm as lgb
# import ipywidgets as widgets
# import plotly.express as px
# from keplergl import KeplerGl
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression


def replace_NaN_matching(args: dict) -> dict:
    """
        Replace matched NaNs with source vals

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * source_df (pd.DataFrame): initial dataframe
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    args['source_df'] = df.copy()
    df.loc[df.lon_match.isna(), 'lon_match'] = df.lon
    df.loc[df.lat_match.isna(), 'lat_match'] = df.lat
    args['df'] = df
    return args


def lon_lat_2_x_y(args: dict) -> dict:
    """
        Matched lon & lat -> x & y

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    gdf = gpd.GeoDataFrame(df,
                           geometry=gpd.points_from_xy(df.lon_match,
                                                       df.lat_match),
                           crs="EPSG:4326").to_crs('EPSG:3414')
    df.insert(df.shape[1], 'x', gdf.geometry.x)
    df.insert(df.shape[1], 'y', gdf.geometry.y)
    del df['geometry']
    del gdf
    args['df'] = df
    return args


def compute_velocity(args: dict) -> dict:
    """
        Computes velocity for truck based on current & previouse point.

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']

    # 1. Computing velocity
    distance = (df.loc[:, ['x', 'y']] -
                df.loc[:, ['x', 'y']].shift(-1)).fillna(0)
    time = np.abs((df.loc[:, 'unixtime'] -
                   df.loc[:, 'unixtime'].shift(-1)).fillna(-5))
    velocity = pd.Series(map(lambda d, t: np.linalg.norm(d, 2) / t,
                             distance.values, time))

    df['velocity'] = velocity.copy()
    del distance
    del time
    del velocity
    args['df'] = df.copy()
    return args


def add_velocity_lag(args: dict) -> dict:
    """
        Function adds as new column velocities in previous points

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']

    for i in range(1, 5):
        colname = f'velocity_lag_{i}'

        # Selection latest not missing value
        last_value = df.velocity[~df.velocity.isna()]
        last_value = last_value[len(last_value)-1]

        if colname not in df.columns:
            df.insert(df.shape[1], colname, df.velocity.shift(-i))
        else:
            df.loc[:, colname] = df.velocity.shift(-i)

        df.loc[df.loc[:, colname].isna(), colname] = last_value

    del last_value
    args['df'] = df
    return args


def slice_dataframe(args: dict) -> dict:
    """
        Slices dataframe columns

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    columns = ['speed', 'outlier', 'velocity', 'velocity_lag_1',
               'velocity_lag_2', 'velocity_lag_3', 'velocity_lag_4']
    args['df'] = args['df'].loc[:, columns]
    return args


def replace_inf(args: dict) -> dict:
    """
        Replaces infinite numbers

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    max_val = df.speed[(df.speed != np.inf)].max()
    df.speed = df.speed.replace(np.inf, max_val)
    args['df'] = df
    return args


def fill_na_velocity(args: dict) -> dict:
    """
        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    df.velocity = df.velocity.fillna(0)
    return args


def rehab_speed(args: dict) -> dict:
    """
        Rehabilitates missing values of speed using velocity

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    mask = df.speed.isna()
    df.loc[mask, ['speed']] = \
        args['speed_regr'].predict(df.loc[mask, ['velocity']])
    args['df'] = df
    return args


def predict(args: dict) -> dict:

    args['source_df'] \
        .insert(args['source_df'].shape[1],
                'is_moving',
                args['highway_detection_model'].predict(args['df']))

    del args['df']
    args['df'] = args['source_df'].copy()
    del args['source_df']
    return args
