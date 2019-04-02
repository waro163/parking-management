# -*- coding: utf-8 -*-
import math

Ea = 6378137
Eb = 6356725

def GetRectRange(centerLat,centerLon,distance):
    _,maxLat = GetLatLon(centerLat,centerLon,distance,0)
    _,minLat = GetLatLon(centerLat,centerLon,distance,180)
    maxLon,_ = GetLatLon(centerLat,centerLon,distance,90)
    minLon,_ = GetLatLon(centerLat,centerLon,distance,270)
    return maxLat,minLat,maxLon,minLon

def GetLatLon(lat,lon,distance,angle):
    dx = distance * 1000 * math.sin(angle * math.pi / 180.0)
    dy = distance * 1000 * math.cos(angle * math.pi / 180.0)
    ec = Eb +( Ea - Eb) * (90.0 - lat) / 90.0
    ed = ec * math.cos( lat * math.pi / 180.0)
    newLon = (dx / ed + lon * math.pi /180.0) * 180.0 / math.pi
    newLat = (dy / ec + lat * math.pi /180.0) * 180.0 / math.pi
    return newLon,newLat

def GetRectRange2(centerLat,centerLon,distance):
    maxLat,_ = GetLatLon2(centerLat,centerLon,distance,0)
    minLat,_ = GetLatLon2(centerLat,centerLon,distance,180)
    _,maxLon = GetLatLon2(centerLat,centerLon,distance,90)
    _,minLon = GetLatLon2(centerLat,centerLon,distance,270)
    return maxLat,minLat,maxLon,minLon

# φ is latitude, λ is longitude, θ is the bearing(clockwise from north),
# δ is the angular distance d / R;
# d being the distance travelled, R the earth’s radius
# bearing 方位 0，90，180，270

def GetLatLon2(lat,lon,distance,bearing):
    R = 6378.137
    lat1 = ConvertDegreesToRadians(lat)
    lon1 = ConvertDegreesToRadians(lon)
    bearing1 = ConvertDegreesToRadians(bearing)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) + math.cos(lat1) * math.sin(distance / R) * math.cos(bearing1))
    lon2 = lon1 + math.atan2(math.sin(bearing1) * math.sin(distance / R) * math.cos(lat1),math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))
    lon2 = (lon2 + 3* math.pi) % (2 * math.pi) - math.pi #normalise to -180..+180°

    lat3 = ConvertRadiansToDegrees(lat2)
    lon3 = ConvertRadiansToDegrees(lon2)
    return lat3,lon3

def ConvertDegreesToRadians(degrees):
    return degrees * math.pi / 180.0

def ConvertRadiansToDegrees(radian):
    return radian * 180.0 / math.pi

if __name__ == '__main__':
    latorg = 22.54587746
    lonorg = 114.12873077

    a=GetRectRange(latorg,lonorg,5)
    b=GetRectRange2(latorg,lonorg,5)
    print(a)
    print(b)