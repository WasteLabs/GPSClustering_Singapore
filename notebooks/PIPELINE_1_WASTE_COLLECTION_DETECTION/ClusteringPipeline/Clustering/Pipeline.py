import geopandas as gpd
from sklearn.cluster import DBSCAN


def replace_NaN_matching(args: dict) -> dict:
    """
        Replace matched NaNs with source vals

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * required_columns (list): columns need to be passed to mode
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * source_df (pd.DataFrame): initial dataframe
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * required_columns (list): columns need to be passed to mode
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
                * required_columns (list): columns need to be passed to mode
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)

        Returns:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * required_columns (list): columns need to be passed to mode
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
    """
    df = args['df']
    gdf = gpd.GeoDataFrame(df,
                           geometry=gpd.points_from_xy(df.lon_match,
                                                       df.lat_match),
                           crs="EPSG:4326").to_crs('EPSG:3414')
    df.insert(df.shape[1], 'x_match', gdf.geometry.x)
    df.insert(df.shape[1], 'y_match', gdf.geometry.y)
    del df['geometry']
    del gdf
    args['df'] = df
    return args


def predict(args):
    """
        Args:
            * df (pd.DataFrame): Source data
            * on_cols_to_clust_pred (list<str>): dasdasd
    """
    df = args['df'].copy()
    cols_to_use = args['on_cols_to_clust_pred']

    # 1. Selection records to preprocess
    mask = ~df.is_moving

    # 2. Passing & processing data separation
    X = df.loc[mask, cols_to_use].copy()

    # 3. Cluster_id insertion
    X.insert(X.shape[1], 'cluster_id', -1)

    # 4. Prediction
    X.loc[:, 'cluster_id'] = \
        DBSCAN(eps=args['eps'],
               min_samples=args['min_samples']).fit_predict(X)

    # 5. Interpretation
    df = df.merge(X.loc[:, ['unixtime', 'cluster_id']],
                  how='left', on=['unixtime'])
    df.cluster_id = df.cluster_id.fillna(-1)

    args['df'] = df
    return args
