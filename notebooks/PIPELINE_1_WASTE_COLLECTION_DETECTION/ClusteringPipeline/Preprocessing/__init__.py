import logging
from .HighwayRoadDetection import detect_highway_movements
from .TrafficStuckDetection import detect_traffic_stuck


PIPELINE_FUNCTIONS = [
    detect_highway_movements,
    # detect_traffic_stuck,
]


def __bind_monad(func, args):
    file_info = f"[{args['filename']}]"
    logging.info(f"{file_info} {func.__name__} start")
    args = func(args)
    logging.info(f"{file_info} {func.__name__} finish")
    return args


def preprocess(argument: dict):
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
