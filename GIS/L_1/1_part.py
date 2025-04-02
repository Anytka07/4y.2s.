import osgeo.ogr 


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
    
    min_lon = 180.0
    max_lon = -180.0
    
    
    for featureNum in range(numFeatures): 
        
        feature = layer.GetFeature(featureNum) 
        geom = feature.GetGeometryRef()
        
        
        if geom.GetGeometryType() == osgeo.ogr.wkbLineString or geom.GetGeometryType() == osgeo.ogr.wkbPolygon:
            
            numPoints = geom.GetPointCount()
            
            
            for i in range(numPoints):
                lon, lat, _ = geom.GetPoint(i)
                print("Точка {} геооб’єкта {} має координати ({}, {})".format(i, featureNum, lon, lat))
                
                
                if lon < min_lon:
                    min_lon = lon
                if lon > max_lon:
                    max_lon = lon
                
            print() 


print("Найзахідніша точка має координати ({}, {})".format(min_lon, lat))
print("Найсхідніша точка має координати ({}, {})".format(max_lon, lat))







