import geopandas as gpd
import os
from shapely.geometry import Point

# -----------1--------------
# Вкажіть шлях до папки з shapefile
extracted_folder = 'D:/4_курс_2_семестр/ГІС/L_2'

# Завантаження векторних даних (shapefile)
shapefile_path = os.path.join(extracted_folder, 'gis_osm_water_a_free_1.shp')
gdf = gpd.read_file(shapefile_path)

# -----------2-------------
# Перевірка CRS та переведення у метричну систему
if gdf.crs != "EPSG:32633":
    gdf = gdf.to_crs(epsg=32633)
print("Проекція після переведення:", gdf.crs)

# -----------3-------------
# Обчислення площі
gdf['area'] = gdf.geometry.area
print(gdf[['name', 'area']])

# Завантаження доріг
roads = gpd.read_file(os.path.join(extracted_folder, "gis_osm_roads_free_1.shp"))
roads = roads.to_crs(epsg=32633)  # Переконатися, що координати правильні
roads['length'] = roads.geometry.length
total_length = roads['length'].sum()
print(f"Загальна довжина доріг: {total_length} м")

# Завантаження точкових об'єктів (POI)
points = gpd.read_file(os.path.join(extracted_folder, "gis_osm_pois_a_free_1.shp"))
points = points.to_crs(epsg=32633)  # Переконатися, що координати правильні

# Завантаження адмін. межі 
admin_boundary = gpd.read_file(os.path.join(extracted_folder, "gis_osm_places_a_free_1.shp"))
#print(admin_boundary["name"].unique())

admin_boundary = admin_boundary.to_crs(epsg=32633)

# Фільтрація по регіону "Општина Србица" 
selected_admin = admin_boundary[admin_boundary['name'] == 'Општина Србица']

if selected_admin.empty:
    print("Помилка: Адміністративна одиниця 'Општина Србица' не знайдена.")
else:
    points_within_admin = points[points.geometry.within(selected_admin.geometry.union_all())]
    print("Точки в межах адміністративної одиниці:")
    print(points_within_admin[['name', 'geometry']])

# Пошук точок у радіусі 1 км від річки
water = gpd.read_file(os.path.join(extracted_folder, "gis_osm_waterways_free_1.shp"))
water = water.to_crs(epsg=32633)  # Правильна проекція

buffered_water = water.geometry.buffer(1000)  # 1000 м = 1 км
points_near_water = points[points.geometry.within(buffered_water.union_all())]
print("Точки поблизу водного об'єкта:")
print(points_near_water[['name', 'geometry']])

# -----------4-------------
import matplotlib.pyplot as plt

import folium
from shapely.geometry import mapping

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx  # Для додавання растрового шару

# --- Візуалізація багатошарової карти ---
fig, ax = plt.subplots(figsize=(10, 10))

# Додавання растрової підкладки
ctx.add_basemap(ax, crs=roads.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_xlim([roads.total_bounds[0], roads.total_bounds[2]])
ax.set_ylim([roads.total_bounds[1], roads.total_bounds[3]])
ax.set_aspect('equal')

buffered_water = gpd.GeoDataFrame(geometry=buffered_water, crs=water.crs)

# Візуалізація буферних зон навколо водних об'єктів (1 км)
buffered_water.plot(ax=ax, color='cyan', alpha=0.3, label='Буферна зона (1 км)')

# Візуалізація водних об'єктів
water.plot(ax=ax, color='blue', alpha=0.5, label="Водні об'єкти")

# Візуалізація доріг
roads.plot(ax=ax, color='gray', linewidth=0.7, label='Дороги')

# Візуалізація адміністративних меж
selected_admin.plot(ax=ax, color='none', edgecolor='black', linewidth=2, label='Адміністративна одиниця')

# Візуалізація точок (POI)
if not points_within_admin.empty:
    points_within_admin.plot(ax=ax, color='red', markersize=20, label='Точки в межах адміністративної одиниці')

# Додавання легенди та підпису
plt.legend()
plt.title("Багатошарова карта з растровим фоном")
plt.show()

