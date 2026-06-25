#### This script averages values within each 0.25° ERA5 grid cell, 
#### resulting in several hourly mean observations contributing to each grid-cell average
import xarray as xr
import numpy as np
import pandas as pd

#### Parameters ####
## ds_obs: observation dataframe (xarray dataset)
## ds_era5: era5 dataframe (xarray dataset)
## time_dim: time dimension (e.g. "Time"; String)

#### Returns ####
## ds_obs_mean: dataframe of grid cell averaged observations (xarray dataset)
## era5_mean_on_obs: dataframe of grid cell averaged ERA5 (xarray dataset)

def collocate_obs_to_era5(ds_obs, ds_era5, time_dim):

    ## resample to hourly
    ds_obs_1h = ds_obs.resample(time="1h", label="right", closed="right").mean()

    ## Define ERA lat-lon grid
    lat_era5 = ds_era5.latitude
    lon_era5 = ds_era5.longitude

    ## Find nearest ERA5 grid point for each observation
    lat_bin = np.round(lat_era5.sel(latitude=ds_obs_1h.lat, method="nearest").data, 4)
    lon_bin = np.round(lon_era5.sel(longitude=ds_obs_1h.lon+360, method="nearest").data, 4)

    ds_era_grid = ds_obs_1h.assign_coords(
    lat_bin=(time_dim, lat_bin),
    lon_bin=(time_dim, lon_bin)
    )
    ## take observarion mean
    ds_obs_mean = ds_era_grid.groupby(
        ["lat_bin", "lon_bin"]
    ).mean(time_dim)

    ## find matching era5
    era5_time = ds_era5.time.sel(
    time=ds_era_grid[time_dim],
    method="nearest"
    )

    ds_era_grid = ds_era_grid.assign_coords(
    era5_time=(time_dim, era5_time.data)
    )
        

    ## now find closest ERA5 gridpoint to each observation 
    era5_sampled = ds_era5.sel(time=ds_era_grid.era5_time, latitude=ds_era_grid.lat_bin, longitude=ds_era_grid.lon_bin, method="nearest")

    ## assign lat and lon coordinates
    era5_sampled = era5_sampled.assign_coords( lat_bin=(time_dim, ds_era_grid.lat_bin.data), lon_bin=(time_dim, ds_era_grid.lon_bin.data))

    ## group by lat lon
    era5_mean_on_obs = (era5_sampled .groupby(("lat_bin", "lon_bin")) .mean(time_dim))

    ## return dataframes
    return ds_obs_mean,  era5_mean_on_obs
