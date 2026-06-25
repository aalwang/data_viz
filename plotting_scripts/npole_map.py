## Script for making north polar stereographic maps with shading and line contours

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.path as mpath
import cartopy.feature as cfeature
import numpy as np
from cartopy.util import add_cyclic_point
from matplotlib.colors import BoundaryNorm
import xarray as xr

## for interactive plotting
import geoviews as gv
import hvplot.xarray
gv.extension('bokeh')

## ax: Axis for plotting (ax object)
## lat = data latitude (numpy array)
## lon = data longitude (numpy array)
## var = shaded field (numpy array)
## var_cont = contour field (numpy array)
## region: Define domain (e.g. [-180,180,45,90])
## levels: levels for shaded field (list of floats)
## levels_cont: levels for line contours (list of floats)
## cmap: colormap (cmap object)
## norm: True when a normalized colorbar is needed (boolean)
## circle: True when circular plot shape is desired (boolean)
## landmask: True when land mask is desired (boolean)
## odd_grid: True when plotting native grid with odd lat long values. For these, cyclical point is not needed. (boolean)
## interactive: True for interacive plotting (boolean)

def npole_map(ax, lat,lon,var,var_cont,region,levels,levels_cont,cmap,norm,circle,landmask,odd_grid,interactive):
    if interactive==True:

        ## convert to DataArray if numpy array supplied
        if not isinstance(var, xr.DataArray):

            var = xr.DataArray(
                var,
                coords={'lat': lat, 'lon': lon},
                dims=['lat', 'lon']
            )

        return var.hvplot(
            x='lon',
            y='lat',
            geo=True,
            #projection=ccrs.NorthPolarStereo(),
            coastline=True,
            cmap=cmap,
            clim=(levels[0], levels[-1]),
            rasterize=True,
            frame_width=700,
            frame_height=700,
            tools=['hover'],
            title='Interactive Polar Map'
        )
    if interactive==False:
        ## handle cyclical point
        if odd_grid==False:
            var, lon = add_cyclic_point(var,coord=lon)
            
            ## apply cyclical point to contours if present
            if var_cont is not None:
                var_cont, _ = add_cyclic_point(var_cont, coord=lon[:-1])
    
        ax.coastlines(linewidth=0.5)
        ax.set_extent(region,crs=ccrs.PlateCarree())
        
        if odd_grid==False:
            norm = BoundaryNorm(levels, ncolors=cmap.N)
            if norm == True:
                cf = ax.contourf(lon,lat,var,levels=levels,transform=ccrs.PlateCarree(),
                norm=norm,cmap=cmap)
            else:
                cf = ax.contourf(lon,lat,var,levels=levels,transform=ccrs.PlateCarree(),
                cmap=cmap)

            if var_cont is not None:
                c = ax.contour(var_cont.longitude,var_cont.latitude,var_cont,levels_cont,transform=ccrs.PlateCarree(),
                colors='k',linewidths=2)
                ax.clabel(c, inline=True,levels=c.levels[::2], inline_spacing=1,fontsize=15)
        if odd_grid==True:
            norm = BoundaryNorm(levels, ncolors=cmap.N)
            if norm == True:
                cf = ax.pcolormesh(lon,lat,var,transform=ccrs.PlateCarree(),
                norm=norm,cmap=cmap)
            else:
                cf = ax.pcolormesh(lon,lat,var,transform=ccrs.PlateCarree(),
                cmap=cmap)

            if var_cont is not None:
                c = ax.contour(var_cont.longitude,var_cont.latitude,var_cont,levels_cont,transform=ccrs.PlateCarree(),
                colors='k',linewidths=2)
                ax.clabel(c, inline=True,levels=levels_cont, inline_spacing=1,fontsize=15)
        ## Add Colorbar
        cb = plt.colorbar(cf, orientation='horizontal',fraction=0.046, pad=0.04)
        cb.ax.tick_params(labelsize=22)
                
    if landmask == True:
        ax.add_feature(cfeature.LAND, zorder=50, facecolor="darkgray")
    
    ## Add lat and lon
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                  linewidth=1, color='k', alpha=0.5, linestyle='--')

    gl.xlabels_top = False # Disable top x-labels
    gl.ylabels_right = False # Disable right y-labels

    
    ## If you want the plot to be circular
    if circle==True:
             theta  = np.linspace(0, 2*np.pi, 100)
             center = [0.5, 0.5]
             radius =  0.5
             verts  = np.vstack([np.sin(theta), np.cos(theta)]).T
             circle = mpath.Path(verts * radius + center)
             ax.set_boundary(circle, transform=ax.transAxes)
    return ax