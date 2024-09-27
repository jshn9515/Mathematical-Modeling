import numpy as np
import pandas as pd
import scipy.interpolate as spi
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
from cartopy.mpl.geoaxes import GeoAxes

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_excel('附件2-站点编号.xlsx')
station = df['站点名称'].values
lon = df['经度(度)'].to_numpy()
lat = df['纬度(度)'].to_numpy()
altitude = df['高度(m)'].to_numpy()
num = 100
x = np.linspace(np.min(lon), np.max(lon), num=num)
y = np.linspace(np.min(lat), np.max(lat), num=num)
x, y = np.meshgrid(x, y)
z = spi.griddata((lon, lat), altitude, (x, y), method='cubic')
z = np.ma.masked_less(z, value=0)
fig = plt.figure(1)
ax = fig.add_subplot(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND.with_scale('10m'), edgecolor='black')
ax.add_feature(cfeature.OCEAN.with_scale('10m'))
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.STATES.with_scale('10m'))
h = ax.contour(x, y, z, levels=10, vmin=0)
ax.clabel(h, fmt='%d', inline=True, inline_spacing=5, fontsize=10)
ax.scatter(lon, lat, c='black', s=10)
for i in range(df.shape[0]):
    ax.annotate(station[i], (lon[i], lat[i]), textcoords='offset points', xytext=(0, 8),
                horizontalalignment='center', fontsize=12)
ax.set_extent([np.min(lon) - 0.5, np.max(lon) + 0.5, np.min(lat) - 0.5, np.max(lat) + 0.5])
ax.xaxis.set_major_formatter(cticker.LongitudeFormatter())
ax.yaxis.set_major_formatter(cticker.LatitudeFormatter())
plt.show()
