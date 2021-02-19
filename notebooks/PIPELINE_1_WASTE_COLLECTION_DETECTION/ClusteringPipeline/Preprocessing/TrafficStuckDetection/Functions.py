import numpy as np


def __enumerate_sequence(df, col, is_true):
    # 1. Lets compute start & end mask
    seq_begin = ((df.loc[:, col] != is_true) &
                 (df.loc[:, col].shift(-1) == is_true)).shift(1)
    seq_end = ((df.loc[:, col] == is_true) &
               (df.loc[:, col].shift(-1) != is_true)).shift(1)

    # 2. First & last records are always False
    if is_true:
        seq_begin[0] = False
        seq_end[0] = False
    else:
        seq_begin[0] = True
        seq_end[0] = False
        seq_end[seq_end.shape[0]] = True

    # 2. Get indexes of sequence beginning and ending
    seq_begin = list(seq_begin[seq_begin].index)
    seq_end = list(seq_end[seq_end].index)

    # 3. Generation of sequence id
    seq_id = list(range(len(seq_begin)))

    # 4. Enumeration
    col_name = f"{is_true}_seq_id"
    df.insert(df.shape[1], col_name, np.NaN)
    for _id, begin, end in zip(seq_id, seq_begin, seq_end):
        df.loc[((df.index >= begin) & (df.index < end)), col_name] = _id

    return df


def aggregate_legs(args: dict) -> dict:
    """
        Function enumerating & aggregating False leg sequences.
    """
    # 1. Enumeration
    df = __enumerate_sequence(args['df'].copy(), 'is_moving', False)

    # 2. Aggregation
    df['amount'] = 1
    args['aggregates'] = df.groupby(['False_seq_id']) \
        .agg({'amount': 'count'}).reset_index()

    args['df'] = df.copy()
    del df

    return args


def predict_on_aggregates(args):
    """
        Performs prediction if truck is stuck in traffic
        on aggregated table

        NOTE: this is huge area for research
    """
    df = args['aggregates']

    df.insert(df.shape[1], 'is_traffic_stuck',
              df.amount < args['max_points_in_traffic_stuck'])

    args['aggregates'] = df
    return args


def interpret_predictions(args):
    """
        Interprets back predictions
    """
    df = args['df']
    df = df.merge(args['aggregates'],
                  on=['False_seq_id'], how='left')

    # 1. Missing values handling
    df.loc[df.is_traffic_stuck.isna(), 'is_traffic_stuck'] = False
    df.is_traffic_stuck = df.is_traffic_stuck.astype('bool')

    args['df'] = df
    del args['df']['False_seq_id']
    del args['df']['amount_x']
    del args['df']['amount_y']
    del args['aggregates']
    return args
