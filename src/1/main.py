import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from src.constants import BACKGROUND_COLOR, CMAP_DIVERGING

"""
For labels with automatic text alignment, use:

from adjustText import adjust_text

from src.constants import SECONDARY_COLOR

texts = list(karls_gdf.apply(
    lambda x: plt.text(x.geometry.x, x.geometry.y, x['Kohanimi'], fontsize=5),
    axis=23
))

adjust_text(texts, arrowprops=dict(arrowstyle="-", color=SECONDARY_COLOR, lw=0.3))
"""

counties = gpd.read_file('../../common_data/maakonnad/maakond.shp')
karls_df = pd.read_csv('data/karlid.csv', delimiter=';')
karls_gdf = gpd.GeoDataFrame(
    karls_df,
    geometry=gpd.points_from_xy(x=karls_df['Y'], y=karls_df['X'], crs='EPSG:3301')
)

base = counties.plot(color=BACKGROUND_COLOR)
karls_map = karls_gdf.plot(column='Nimeobjekti liik', categorical=True, cmap=CMAP_DIVERGING, ax=base, marker='.',
                           markersize=20, legend=True, legend_kwds={'loc': 'upper left', 'title': 'Objekti liik'})

plt.title('Kohad, mille nimes sisaldub "Karl"')
plt.axis('off')
plt.show()
