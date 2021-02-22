# Models

## fast_movement_detector.sav

* **Source notebook**: `notebooks/PIPELINE_1_WASTE_COLLECTION_DETECTION/01_FAST_MOVEMENT_MODELING.ipynb`

```python
# Experiment history
[({}, 0.916158821331839), # X = ['velocity']
 ({}, 0.9294503595778464), # X = ['velocity', 'velocity_lag_1']
 ({}, 0.9418429532081813), # X = ['velocity', 'velocity_lag_1', 'velocity_lag_2']
 ({}, 0.9642757074810869), # X = ['velocity', 'velocity_lag_1', 'velocity_lag_2', 'velocity_lag_3']
 ({}, 0.9737613243672363), # X = ['velocity', 'velocity_lag_1', 'velocity_lag_2', 'velocity_lag_3', 'velocity_lag_4']
 ({}, 0.9772228448678435), # X = ['velocity', 'velocity_lag_1', 'velocity_lag_2', 'velocity_lag_3', 'velocity_lag_5']
 ({}, 0.9772228448678435)] # X = ['velocity', 'velocity_lag_1', 'velocity_lag_2', 'velocity_lag_3', 'velocity_lag_5', 'velocity_lag_6']
```

* **X**: `['velocity', 'velocity_lag_1', 'velocity_lag_2', 'velocity_lag_3', 'velocity_lag_5']`
* **y**(bool): is moving fast or not?
