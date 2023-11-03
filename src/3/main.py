import geopandas as gpd
from matplotlib import pyplot as plt

from src.constants import BACKGROUND_COLOR

countries = gpd.read_file('../../common_data/maailm.zip')
countries['geometry'] = countries['geometry'].simplify(1000)
base = countries.plot(color=BACKGROUND_COLOR)

plt.title('Maailm Tesla Cybertruckina', fontsize=7)
plt.axis('off')
plt.savefig('result.png', dpi=300, bbox_inches='tight')
