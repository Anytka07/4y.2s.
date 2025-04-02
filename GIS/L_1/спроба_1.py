import osgeo.ogr 
from geopy.distance import geodesic


shapefile = osgeo.ogr.Open("UKR_rails.shp") 


numLayers = shapefile.GetLayerCount() 
print("Файл фігур містить {} шарів".format(numLayers))
print()


for layerNum in range(numLayers): 
    layer = shapefile.GetLayer(layerNum) 
    
    
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    
    
    numFeatures = layer.GetFeatureCount() 
    print("шар {} має просторову прив’язку {}".format(layerNum, spatialRef))
    print("шар {} містить {} геооб’єктів: ".format(layerNum, numFeatures)) 
    print() 
    
  
    count = 0
    
    
    for featureNum in range(numFeatures): 
        
       
        if count >= 20:
            break
        
        feature = layer.GetFeature(featureNum) 
        
       
        geom = feature.GetGeometryRef()
        lon = geom.GetX()
        lat = geom.GetY()
        
       
        print("Геооб’єкт {} має координати ({}, {})".format(featureNum, lon, lat))

        prev_lon, prev_lat = lon, lat
        
        
        count += 1
        
        print() 


