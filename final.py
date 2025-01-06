import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from libpysal.weights import KNN
from esda.getisord import G_Local
df = pd.read_csv('starbucks_data.csv')

df = df[df['Country'] == 'TR']
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
gdf.set_crs(epsg=4326, inplace=True)  
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='green', markersize=5, alpha=0.6, edgecolor='k')
ctx.add_basemap(ax, source='https://tile.openstreetmap.org/{z}/{x}/{y}.png', crs=gdf.crs)
plt.title('Starbucks Mağazaları - Türkiye')
plt.show()

w = KNN.from_dataframe(gdf, k=8)
w.transform = 'r'

gdf['Gi*'] = G_Local(gdf['geometry'].y, w).Zs

gdf['Gi*'] = gdf['Gi*'] - gdf['Gi*'].min()

fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(column='Gi*', cmap='RdBu_r', legend=True, ax=ax, markersize=20, alpha=0.7)
ctx.add_basemap(ax, source='https://tile.openstreetmap.org/{z}/{x}/{y}.png', crs=gdf.crs)
plt.title('Starbucks Mağazaları - Hot-Spot Analizi (Getis-Ord Gi*)')
plt.show()

fig.savefig('starbucks_hotspot_turkey.png', dpi=300)
gdf.to_file('starbucks_turkey_hotspot.geojson', driver='GeoJSON')



