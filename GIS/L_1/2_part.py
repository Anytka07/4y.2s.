import osgeo.ogr 


shapefile = osgeo.ogr.Open("UKR_rails.shp") 

layer = shapefile.GetLayer(0) 

feature = layer.GetFeature(27)

geom = feature.GetGeometryRef()


numPoints = geom.GetPointCount()
total_lon = 0
total_lat = 0
for i in range(numPoints):
    lon, lat, _ = geom.GetPoint(i)
    total_lon += lon
    total_lat += lat


central_lon = total_lon / numPoints
central_lat = total_lat / numPoints

print("Центральна точка об'єкту 27 має координати ({}, {})".format(central_lon, central_lat))
