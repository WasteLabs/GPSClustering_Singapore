import logging
from .Pipeline import predict
from .Pipeline import lon_lat_2_x_y
from .Pipeline import replace_NaN_matching


PIPELINE_FUNCTIONS = [
    replace_NaN_matching,
    lon_lat_2_x_y,
    predict,
]


def __bind_monad(func, args):
    file_info = f"[{args['filename']}]"
    logging.info(f"{file_info} {func.__name__} start")
    args = func(args)
    logging.info(f"{file_info} {func.__name__} finish")
    return args


def clusterize(argument: dict):
    """
        Entry point function to module

        Args:
            (dict):
                * filename (str): name of processing file
                * df (pd.DataFrame)
                * speed_fill (sklearn.LinearRegression): linear regression
                                                        (x - velocity,
                                                         y - speed)
        Outputs:
            (pd.DataFrame):
                * is_moving (bool):
                    (True): Car is moving on speed speed not
                            similar to potential waste collection
                    (False):
                        - Truck is stuck in traffic
                        - Collecting the waste
                        - Doing something weird
    """
    logging.info("\n")
    for function in PIPELINE_FUNCTIONS:
        argument = __bind_monad(function, argument)
    return argument
