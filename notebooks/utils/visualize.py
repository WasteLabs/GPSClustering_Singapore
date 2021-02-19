cols2visualize = list(anomalies_l2_agg.loc[:, 'l2_percentile_0': 'l2_percentile_100'].columns)

# 1. Percentile distributions
fig = px.line(anomalies_l2_agg, x="date_gps",
              y=cols2visualize, title='l2 distance of RFID and GPS by percentiles')
fig.show()

# 2. Standard deviation
fig = px.line(anomalies_l2_agg, x="date_gps",
              y='l2_distance_std', title='standard deviation of l2 distance of RFID and GPS')
fig.show()
