import pickle
from .Preprocessing import preprocess
from .Clustering import clusterize


def do_clustering(df, eps, min_samples,
                  is_moving_log_reg_path,
                  speed_rehab_model_path,
                  fname):

    args = {
        'filename': fname,
        'df': df.copy(),
        'speed_regr': pickle.load(open(speed_rehab_model_path, 'rb')),
        'highway_detection_model': pickle.load(open(is_moving_log_reg_path,
                                                    'rb')),
        'on_cols_to_clust_pred': ['x_match', 'y_match', 'unixtime'],
        'min_samples': min_samples,
        'eps': eps
    }

    outputs = clusterize(preprocess(args))
    return outputs
