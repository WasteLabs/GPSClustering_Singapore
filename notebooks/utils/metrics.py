import pandas as pd
import numpy as np

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

def describe_l2(anomalies: pd.DataFrame) -> pd.DataFrame:
    anomalies_l2_agg = anomalies.groupby(['date_gps']).agg(l2_distance_mean=('l2_distance', 'mean'),
                                                            l2_distance_std=('l2_distance', 'std'),
                                                            l2_distance_min=('l2_distance', 'min'),
                                                            l2_distance_max=('l2_distance', 'max'),
                                                            l2_percentile_0=('l2_distance', percentile(0)),
                                                            l2_percentile_10=('l2_distance', percentile(10)),
                                                            l2_percentile_20=('l2_distance', percentile(20)),
                                                            l2_percentile_30=('l2_distance', percentile(30)),
                                                            l2_percentile_40=('l2_distance', percentile(40)),
                                                            l2_percentile_50=('l2_distance', percentile(50)),
                                                            l2_percentile_60=('l2_distance', percentile(60)),
                                                            l2_percentile_70=('l2_distance', percentile(70)),
                                                            l2_percentile_80=('l2_distance', percentile(80)),
                                                            l2_percentile_90=('l2_distance', percentile(90)),
                                                            l2_percentile_100=('l2_distance', percentile(100)),
                                                   ).reset_index()
    return anomalies_l2_agg

def describe_unixtime_delta(anomalies):
    anomalies_t_delta_agg = anomalies.groupby(['date_gps']).agg(unixtime_delta_mean=('delta_unixtime', 'mean'),
                                                                unixtime_delta_std=('delta_unixtime', 'std'),
                                                                unixtime_delta_min=('delta_unixtime', 'min'),
                                                                unixtime_delta_max=('delta_unixtime', 'max'),
                                                                unixtime_delta_0=('delta_unixtime', percentile(0)),
                                                                unixtime_delta_10=('delta_unixtime', percentile(10)),
                                                                unixtime_delta_20=('delta_unixtime', percentile(20)),
                                                                unixtime_delta_30=('delta_unixtime', percentile(30)),
                                                                unixtime_delta_40=('delta_unixtime', percentile(40)),
                                                                unixtime_delta_50=('delta_unixtime', percentile(50)),
                                                                unixtime_delta_60=('delta_unixtime', percentile(60)),
                                                                unixtime_delta_70=('delta_unixtime', percentile(70)),
                                                                unixtime_delta_80=('delta_unixtime', percentile(80)),
                                                                unixtime_delta_90=('delta_unixtime', percentile(90)),
                                                                unixtime_delta_100=('delta_unixtime', percentile(90)),
                                                   ).reset_index()
    return anomalies_t_delta_agg
