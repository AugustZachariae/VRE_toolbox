# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:24:57 2020

@author: Bruger
"""


def to_clipboard(array, decimal=","):
    """
    Copies an array into a string format acceptable by Excel.
    Columns separated by \t, rows separated by \n
    """
    import numpy as np
    import win32clipboard as clipboard
    # Create string from array
    try:
        n, m = np.shape(array)
    except ValueError:
        n, m = 1, 0
    line_strings = []
    if m > 0:
        for line in array:
            if decimal == ",":
                line_strings.append("\t".join(line.astype(str)).replace(
                    "\n","").replace(".", ","))
            else:
                line_strings.append("\t".join(line.astype(str)).replace(
                    "\n",""))
        array_string = "\r\n".join(line_strings)
    else:
        if decimal == ",":
            array_string = "\r\n".join(array.astype(str)).replace(".", ",")
        else:
            array_string = "\r\n".join(array.astype(str))
    # Put string into clipboard (open, clear, set, close)
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardText(array_string)
    clipboard.CloseClipboard()
def readcsv(filename, deliminator):
    """ Function to read csv files, option to choose deliminator """
    import numpy as np
    import csv
    
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=deliminator)
        headers = next(reader)
        
        
        datatmp = np.array(list(reader))
        
        try:
            datatmp = datatmp.astype(float)
            
        except:
            print('not float')
    
    return datatmp, headers

def hour2date(windTimeHour):
    """ Function to convHoursert array of hours since 1900,1,1 to dates """
    import datetime as dt
    import numpy as np
    
    windSize = np.size(windTimeHour)
    
    dtstart = dt.datetime(1900,1,1,0,0,0)
    windTimeDate = np.zeros(windSize, dtype = 'datetime64[us]')
    
    for i in range(0,windSize):
        
        windTimeDate[i] = dtstart + dt.timedelta(0,0,0,0,0,int(windTimeHour[i]))
        
    return windTimeDate

def getGrid(windLat, windLon):
    """ Function to get ERA5 Lat Lon in grid format """
    import numpy as np
    
    latSize = np.size(windLat)
    lonSize = np.size(windLon)
    windGridLat = np.zeros((latSize,lonSize))
    windGridLon = np.zeros((latSize,lonSize))
    
    for i in range(0,lonSize):
        for j in range(0, latSize):
            windGridLat[j,i] = windLat[j]
            windGridLon[j,i] = windLon[i]
            
    return windGridLat, windGridLon

def latlon2m(lat, lon):
    """ Function to convert lat lon to utm zone 32 in meters"""
    # Note, pyproj returns lon lat
    import numpy as np
    from pyproj import Proj
    
    if np.size(lat) > 1:
        p = Proj(proj="utm",zone=32,ellps="WGS84", datum = "WGS84", south=False)
        x, y= p(lon.ravel(),lat.ravel())
        
    else:
        p = Proj(proj="utm",zone=32,ellps="WGS84", datum = "WGS84", south=False)
        x, y= p(lon,lat)
    
    return x, y

def createDataStruct():
    from typing import NamedTuple

    class windData(NamedTuple):
        time: int
        datetime: str
        speed: float
        hgt: int
        size: int
        lat: float
        lon: float
        x: float
        y: float
        subspeed: float
        tmpindex: float
        
    return windData