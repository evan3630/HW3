#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 16:14:53 2023

@author: evanchladny
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from cartopy import crs as ccrs
from cartopy.util import add_cyclic_point

# Read in the Data 
fname='Global Data'
ds=xr.open_dataset(fname)
print(ds)

#Create the plot

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution='50m')


central_lon, central_lat = 0, 55
extent = [-15, 15, 64, 46]
ax.set_extent(extent)
ax.coastlines(resolution='50m')

wind = np.sqrt((ds['u10'].squeeze()*ds['u10'].squeeze()) + (ds['v10'].squeeze()*ds['v10'].squeeze()))

wind_cyc, lon_cyc = add_cyclic_point(wind, coord=ds['longitude'])

cs = ax.contourf(lon_cyc, 
              ds['latitude'], 
              wind_cyc,
              transform = ccrs.PlateCarree(),extend='both', cmap = 'inferno_r', levels = [10, 12, 14, 16, 18, 20], alpha = 0.6)

ax.quiver(ds['longitude'][::7], ds['latitude'][::7], ds['u10'][0, ::7, ::7], ds['v10'][0, ::7, ::7], scale = 350, width = 0.004)

cbar = plt.colorbar(cs,orientation='horizontal', label = '10-m Wind speed [m s$^{-1}$]', shrink = 0.8, pad = 0.05)

plt.savefig('my_figure.pdf', bbox_inches='tight', dpi=400)