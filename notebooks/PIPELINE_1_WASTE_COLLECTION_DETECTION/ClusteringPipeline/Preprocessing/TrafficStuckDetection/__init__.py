import logging
from .Functions import aggregate_legs
from .Functions import predict_on_aggregates
from .Functions import interpret_predictions


PIPELINE_FUNCTIONS = [
    aggregate_legs,
    predict_on_aggregates,
    interpret_predictions
]


def __bind_monad(func, args):
    file_info = f"[{args['filename']}]"
    logging.info(f"{file_info} {func.__name__} start")
    args = func(args)
    logging.info(f"{file_info} {func.__name__} finish")
    return args


def detect_traffic_stuck(argument: dict):
    """
        Entry point function to module

        Args:
            (dict):
                * max_points_in_traffic_stuck (int): maximum amount of points
                                                     False to consider as
                                                     traffic stuck.
                * df (pd.DataFrame):
    """
    logging.info("\n")
    for function in PIPELINE_FUNCTIONS:
        argument = __bind_monad(function, argument)
    return argument
