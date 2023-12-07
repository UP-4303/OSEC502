# -*- coding: utf-8 -*-
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

def getDt(dist):
    # pour le temps mis par l'onde pour aller du foyer à la station
    V1 = 6   # avec V1 en Km/s qui correspondent aux ondes P
    V2 = 3.5   # avec V2 en Km/s qui correspondent aux ondes S

    # tp = temps d'arrivée des ondes P et ts = temps d'arrivée des ondes S

    tp = (dist / V1)
    ts = (dist / V2)
    
    # pour obtenir le dt on soustrait ts à tp

    # dt = ts - tp
    return tp

if (__name__  == '__main__'):

    dist = distance(lon1, lat1, lon2, lat2)/1000
    print(f'la distance entre le foyer et la station la plus proche est {dist} ')
    
    dt = getDt(dist)

    print(f'le temps de parcours des ondes p est {tp} en min')
    print(f'le temps de parcours des ondes s est {ts} en min')
    print(f'donc dt vaut (dt) en min') 
