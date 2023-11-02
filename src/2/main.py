import geopandas as gpd
from adjustText import adjust_text
from matplotlib import pyplot as plt
from shapely import box

from src.constants import BACKGROUND_COLOR, MAIN_COLOR, SECONDARY_COLOR

cables = gpd.read_file('data/cables.geojson')
landing_points = gpd.read_file('data/landing-points.geojson')

landing_points['points'] = landing_points['geometry']
landing_points['geometry'] = landing_points.geometry.buffer(.1)

points_from_tallinn = landing_points[landing_points['name'] == 'Tallinn, Estonia']
cables_from_tallinn = gpd.sjoin(cables, points_from_tallinn, how='inner', op='intersects')
cables_from_tallinn = cables_from_tallinn[['color', 'slug_left', 'geometry']]
points_from_tallinn = gpd.sjoin(landing_points, cables_from_tallinn, how='inner', op='intersects')
points_from_tallinn = points_from_tallinn[['slug_left', 'name', 'id', 'geometry', 'points']]

cables_n = len(cables_from_tallinn.index)

while True:
    cables_from_tallinn = gpd.sjoin(cables, points_from_tallinn, how='inner', op='intersects').drop_duplicates()
    cables_from_tallinn = cables_from_tallinn[['color', 'slug_left', 'geometry']]
    points_from_tallinn = gpd.sjoin(landing_points, cables_from_tallinn, how='inner', op='intersects').drop_duplicates()
    points_from_tallinn = points_from_tallinn[['slug_left', 'name', 'id', 'geometry', 'points']]

    new_cables_n = len(cables_from_tallinn.index)
    if cables_n == new_cables_n:
        break
    cables_n = new_cables_n

points_from_tallinn['geometry'] = points_from_tallinn['points']

countries = gpd.read_file('../../common_data/maailm.zip')
polygon = box(8, 53.5, 32.7, 61.7)  # Extent of map
countries = countries.clip(polygon)

base = countries.plot(color=BACKGROUND_COLOR)
cables_from_tallinn.plot(ax=base, color=SECONDARY_COLOR, linewidth=0.4)
points_from_tallinn.plot(ax=base, color=MAIN_COLOR, markersize=8)

texts = list(points_from_tallinn[['name', 'geometry']].drop_duplicates().apply(
    lambda x: plt.text(x.geometry.x, x.geometry.y, x['name'], fontsize=5),
    axis=1
))

adjust_text(texts)

plt.title('Kuhu on Eestil ühendus merealuste kaablite kaudu', fontsize=7)
plt.axis('off')
plt.savefig('result.png', dpi=300, bbox_inches='tight')
