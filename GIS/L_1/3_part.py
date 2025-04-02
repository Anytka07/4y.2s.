from geopy.distance import geodesic

lon1, lat1 = 33.58930585499999, 51.827194258473384
lon2, lat2 = 31.937360804999994, 51.822082564473384

distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
print("відстань між двома точками: {:.2f} км".format(distance))
