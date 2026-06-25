## function to follow the location of an observation and get the corresponding data from another spatial dataset using linear interpolation

import xarray as xr
import numpy as np
import pandas as pd
from tqdm import tqdm

## data: data we want to find (in our case ERA5) (xarray dataarray)
## t_obs: time of observations (array or series)
## lat_obs: latitude of observation (array or series)
## lon_obs: longitude of observation (array or series)

def follow(data,t_obs,lat_obs,lon_obs):
    
    lon_era5 = (lon_obs + 360) % 360
    data = data.drop_vars('expver', errors='ignore')

    if 'valid_time' in data.coords:
        data = data.rename({'valid_time': 'time'})
    ## create a dataframe to store the corresponding data
    buoy_df = pd.DataFrame({
        'time': t_obs,
        'latitude': lat_obs,
        'longitude': lon_obs,
        'lon_era5': lon_era5
    })

    ## interpolate
    interp_result = data.interp(
        time=("points", np.array(t_obs)),
        latitude=("points", np.array(lat_obs)),
        longitude=("points", np.array(lon_era5)),
        method="linear"
    )
    ## replace points dimension with time
    interp_result = (
        interp_result
        .assign_coords(time=("points", pd.to_datetime(t_obs)))
        .swap_dims({"points": "time"})
    )

    return (interp_result)
