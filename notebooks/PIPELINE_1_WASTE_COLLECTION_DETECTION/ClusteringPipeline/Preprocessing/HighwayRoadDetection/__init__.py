import logging
from .Functions import replace_NaN_matching
from .Functions import lon_lat_2_x_y
from .Functions import compute_velocity
from .Functions import add_velocity_lag
from .Functions import slice_dataframe
from .Functions import replace_inf
# from .Functions import fill_na_velocity
from .Functions import rehab_speed
from .Functions import predict


PIPELINE_FUNCTIONS = [
    replace_NaN_matching,
    lon_lat_2_x_y,
    compute_velocity,
    add_velocity_lag,
    slice_dataframe,
    replace_inf,
    rehab_speed,
    predict
]


def __bind_monad(func, args):
    file_info = f"[{args['filename']}]"
    logging.info(f"{file_info} {func.__name__} start")
    args = func(args)
    logging.info(f"{file_info} {func.__name__} finish")
    return args


def detect_highway_movements(argument: dict):
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
