# -*- coding: utf-8 -

from math import radians, cos, sin, sqrt, atan2

lon1 = -73.9
lat1 = 40.7
lon2 = 2.85
lat2 = 48.75

def distance(lon1,lat1,lon2,lat2):
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    Rt = 6371*1000
    
    dlat = lat2-lat1
    dlon = lon2-lon1
    
    #formule de Haversine
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = Rt * c
    
    return distance

dist=distance(lon1, lat1, lon2, lat2)
print(f'la distance entre le foyer et la station la plus proche est {dist} ')



