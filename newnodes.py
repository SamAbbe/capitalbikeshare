# from internet
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    #r = 6371 # radius of earth in kilometers
    r = 3956 # radius earth use for miles
    return c * r

class LocationType:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
    
    def getLat(self):
        return self.lat
    
    def getLong(self):
        return self.long

    def setLat(self,lat):
        self.lat = lat
    
    def setLong(self,long):
        self.long = long
        
class StationType:
    def __init__(self,lat,long,num):
        self.lat = lat
        self.long = long
        self.id = num
    
    def getLat(self):
        return self.lat
    
    def getLong(self):
        return self.long
    
    def getId(self):
        return self.id
    
import numpy as np
# get lat/long box, divide into xDim x yDim sub-boxes, calculate lat/long for each sub-box
# Lat/Long in decimal format, not D/M/S
maxLat = 38.927
#maxLat = 39.0
maxLong = -77.030
#maxLong = -77.0
#minLat = 38.0
minLat = 38.910
minLong = -77.056
#minLong = -78.0
latDiff = maxLat - minLat
longDiff = maxLong - minLong
xDim = 1000
yDim = 1000
latStep = latDiff / xDim
longStep = longDiff / yDim
print(xDim * yDim," total locations dimensions ", xDim, " by ", yDim)
print("Latitude ", minLat, " to ", maxLat)
print("Longitude ", minLong, " to ", maxLong)
squareMiles = haversine(minLong, minLat, maxLong, minLat) * haversine(minLong, minLat, minLong, maxLat)
printf("Square miles covered ",squareMiles)
printf("Average grid size ",squareMiles / (xDim * yDim))
locationMatrix =  np.zeros( (xDim,yDim), dtype=LocationType )

for i in range(xDim):
    for j in range(yDim):
        #locationMatrix[i,j].setLat(minLat + i * latStep)
        #locationMatrix[i,j].setLong(minLong + i * latLong)
        loc = LocationType(minLat + float(i) * latStep, minLong + float(j) * longStep)
        locationMatrix[i,j] = loc
maxDistance = 0.5
nearestMatrix = np.zeros((xDim,yDim),dtype=np.int16)
stationList = [(38.920669,-77.043680,31113),
               (38.922925,-77.042581,31104),
               (38.924088,-77.040787,31296),
               (38.918808,-77.041571,31114),
               (38.917761,-77.040620,31116),
               (38.915400,-77.044600,31110)]

# CT & Kalorama
proposed1 = (38.918498,-77.04848,1) 
# Kalorama Park
proposed2 = (38.919634,-77.044747,2)
stationList.append(proposed1)
stationList.append(proposed2)


# determine closest station for every entry in matrix
for i in range(xDim):
    for j in range(yDim):
        nearestMatrix[i,j] = 0 # assume no one on range
        minDistance = maxDistance
        loc = locationMatrix[i,j]
        lat = loc.getLat()
        long = loc.getLong()
        for k in range(len(stationList)):
            station = stationList[k]
            stationLat = station[0]
            stationLong = station[1]
            stationId = station[2]
            distance = haversine(stationLong, stationLat, long, lat)
            if distance < minDistance:
                nearestMatrix[i,j] = stationId
                minDistance = distance

# count locations without service (distance > max)
counter = 0
for i in range(xDim):
    for j in range(yDim):
        if nearestMatrix[i,j] == 0:
            counter = counter + 1
print(counter, " locations have no service.")
    
# count occurances for each station
for i in range(len(stationList)):
    currentStation = stationList[i]
    stationId = currentStation[2]
    print("Station # ", stationId, " at ", currentStation[0], currentStation[1])
    counter = 0
    for j in nearestMatrix.flat:
        if stationId == j:
            counter = counter + 1
    print(" Count ",counter)

