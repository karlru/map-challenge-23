import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from src.constants import BACKGROUND_COLOR, MAIN_COLOR

loc_govs = gpd.read_file('../../common_data/omavalitsused/omavalitsus.shp')
base = loc_govs.plot(color=BACKGROUND_COLOR)

kambja = loc_govs[loc_govs['ONIMI'] == 'Kambja vald']
kambja.plot(ax=base, color=MAIN_COLOR)

kambja['centroid'] = kambja.geometry.centroid
kambja = kambja.iloc[0, ]
base.annotate(text=kambja['ONIMI'], xy=(kambja.centroid.x + 10000, kambja.centroid.y), fontsize=7)

legend_elements = [
    Patch(facecolor=MAIN_COLOR, label='Kohad, kus 03.08.2018 kell 13.00 oli soojem kui Gambias*'),
    Patch(facecolor=BACKGROUND_COLOR, label='Kohad, mille temperatuuri kohta 03.08.2018 pole eraldi uudist'),
]
base.legend(handles=legend_elements, loc='upper left', fontsize=7)

plt.text(loc_govs.total_bounds[0], loc_govs.total_bounds[1], '*Postimehe uudiste andmetel', fontsize=4)
plt.axis('off')
plt.savefig('result.png', dpi=300, bbox_inches='tight')
