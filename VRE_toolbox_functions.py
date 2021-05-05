
"""
Created on Tue Dec 22 09:28:04 2020

@author: August Zachariae, Advisor, Danish Energy Agency
This py file contains main functions which can be utilised when working with 
the VRE toolbox. Please proceed with caution if you choose to experiment 
with the functions as some are dependend on each other. 

This file also imports extra "support functions" from the 
VRE_toolbox_support_functions py file. These are functions which are 
unneccesary for the user, but neccessary for important functions to work

"""
from VRE_toolbox_support_functions import *

def map_subset(data,geo_pol):
    import numpy as np
    import json
    import geopandas as gpd
    from shapely.geometry import shape, Point
    from shapely.geometry.polygon import Polygon
    from copy import deepcopy
    # depending on your version, use: from shapely.geometry import shape, Point
    newdata=createDataStruct()
    
    # load GeoJSON file containing sectors
    with open('Indian_states.json') as f:
        js = json.load(f)
    tmp_index=[]

#    geo_pol=Polygon(tuple(js['features'][4]['geometry']['coordinates'][1])[0])
#    geo_pol=Polygon(tuple(js['features'][28]['geometry']['coordinates'][0]))
#    geo_pol=Polygon(tuple(js['features'][16]['geometry']['coordinates'][23])[0])
    for j in range(0,len(data.lon[0,:])):
        for i in range(0,len(data.lon[:,0])):
            if geo_pol.contains(Point(data.lon[i,j],data.lat[i,j])):
                tmp_index.append([i,j])
    tmp_index=np.array(tmp_index)            
    tmp_ind1=tmp_index[:,0]
    tmp_ind2=tmp_index[:,1]
    
    newdata.speed=np.empty_like(data.speed)
    newdata.lon=np.empty_like(data.lon) 
    newdata.lat=np.empty_like(data.lat)
    newdata.x=data.x
    newdata.y=data.y
    newdata.speed[:,:,tmp_ind1,tmp_ind2]=data.speed[:,:,tmp_ind1,tmp_ind2]
    newdata.lon[tmp_ind1,tmp_ind2] = data.lon[tmp_ind1,tmp_ind2]  
    newdata.lat[tmp_ind1,tmp_ind2] = data.lat[tmp_ind1,tmp_ind2]
    newdata.subspeed=data.speed[:,:,tmp_ind1,tmp_ind2]
    newdata.time=data.time
    newdata.datetime=data.datetime
    newdata.hgt=data.hgt
    newdata.size=data.size
    
    return newdata


def wind_var_t(data,RELIB,turbine_index,l_qt,h_qt, hgt_index,h):
    import numpy as np
    data_len = np.shape(data.subspeed)[2]
    data_map = np.zeros(data_len)
    CF=np.zeros((len(data.speed[:,1,1,1])), int)
    
    for i in range(0,data_len):
        
        data_map[i] = np.sum(RELIB[(np.round(data.subspeed[:,hgt_index,i]*100,2)).astype(int),turbine_index])
    
    index=np.where((data_map > np.percentile(data_map, l_qt, interpolation='nearest'))&(data_map < np.percentile(data_map, h_qt, interpolation='nearest'))) 
    
    for i in range(0,len(index[0][:])):
        temp=RELIB[(np.round(data.subspeed[:,hgt_index,index[0][i]]*((h/100) ** 0.143)*100,2)).astype(int),turbine_index]
        CF=np.vstack([CF,temp])  
        
    CF=np.mean(CF,axis = 0)
    
    return CF 


def VRE_VAR_T_quantile(data,RELIB,turbine_index,l_qt,h_qt,quantity, hgt_index):
    import numpy as np
    map_rows = np.shape(data.speed)[2]
    map_cols = np.shape(data.speed)[3]
    
    data_map = np.zeros((map_rows, map_cols)) 
    
    for i in range(0,map_rows):
        for j in range(0,map_cols):
            
            data_map[i,j] = np.mean(RELIB[(np.round(data.speed[:,hgt_index,i,j],2)*100).astype(int),turbine_index])
    index=[] 
    for percentile in np.arange(l_qt, h_qt, ((h_qt-l_qt)/quantity)): 
        index.append(np.where(data_map == np.percentile(data_map, percentile, interpolation='nearest')))
    CF=[]
    for row in index:
        
        CF.append(RELIB[(np.round(data.speed[:,hgt_index,row[0],row[1]],2)).astype(int),turbine_index])  
    CF=np.mean(CF)
    return CF    

def prod_Map_yearly_mean(data, KW, RELIB, turbine_index, hgt_index):
    import numpy as np
    
    map_rows = np.shape(data.speed)[2]
    map_cols = np.shape(data.speed)[3]
    
    data_map = np.zeros((map_rows, map_cols))
    
    for i in range(0,map_rows):
        for j in range(0,map_cols):
            
            data_map[i,j] = np.mean(RELIB[(np.round(data.speed[:,hgt_index,i,j],2)*100).astype(int),turbine_index]*KW)

    return data_map      
        
def getNCData(filename, fileType):
    """ Function to get NetCDF data """
    #from typing import NamedTuple
    import numpy as np
    from netCDF4 import Dataset
    from datetime import datetime

    data = createDataStruct()

    flagError_fileType = 0
    
    rootgrp = Dataset(filename, "r", format="NETCDF4")
    
    if (fileType == 'UERRA') or (fileType == 'uerra'):
        print('UERRA')
        windTime = np.array(rootgrp.variables['time'][:])
        data.time = sec1970tohour1900(windTime)
        data.datetime = hour2date(data.time).astype(object)
        data.lat = np.array(rootgrp.variables['latitude'][:])
        data.lon = np.array(rootgrp.variables['longitude'][:])
        
        data.hgt = np.array(rootgrp.variables['heightAboveGround'][:])
        data.speed = np.array(rootgrp.variables['ws'][:])
        data.size = np.size(data.speed,2)*np.size(data.speed,3)

    
    elif (fileType == 'ERA5') or (fileType == 'era5'):
        print('ERA5')
        data.time = np.array(rootgrp.variables['time'][:])
        data.datetime = hour2date(data.time).astype(object)
        data.lat = np.array(rootgrp.variables['latitude'][:])
        data.lon = np.array(rootgrp.variables['longitude'][:])
        data.lat, data.lon = getGrid(data.lat, data.lon)
        
        windSpeedu10 = np.array(rootgrp.variables['u10'][:])
        windSpeedv10 = np.array(rootgrp.variables['v10'][:])
        windSpeed10 = np.sqrt(windSpeedu10**2 + windSpeedv10**2)
        
        windSpeedu100 = np.array(rootgrp.variables['u100'][:])
        windSpeedv100 = np.array(rootgrp.variables['v100'][:])
        windSpeed100 = np.array(np.sqrt(windSpeedu100**2 + windSpeedv100**2))
        
        data.hgt = [10, 100]
        data.speed = np.array((windSpeed10, windSpeed100))
        data.speed = np.transpose(data.speed, (1, 0, 2, 3))
        
        data.size = np.size(windSpeed100[0])
    
    else:
        flagError_fileType = 1
        print("Unknown data set type. Function only supports UERRA or ERA5")

    rootgrp.close()

    if flagError_fileType != 1:
        data.x, data.y = latlon2m(data.lat,data.lon)
        
        return data

def windspeed_map_avg(data, hgt_index):
    import numpy as np
    
    map_rows = np.shape(data.speed)[2]
    map_cols = np.shape(data.speed)[3]
    
    data_map = np.zeros((map_rows, map_cols))
    
    for i in range(0,map_rows):
        for j in range(0,map_cols):
            
            data_map[i,j] = np.average(data.speed[:,hgt_index,i,j])

    return data_map

def windprod_Map_avg(data, KW, RELIB, turbine_index, hgt_index):
    import numpy as np
    
    map_rows = np.shape(data.speed)[2]
    map_cols = np.shape(data.speed)[3]
    
    data_map = np.zeros((map_rows, map_cols))
    
    for i in range(0,map_rows):
        for j in range(0,map_cols):
            
            data_map[i,j] = np.average(RELIB[(np.round(data.speed[:,hgt_index,i,j],2)*100).astype(int),turbine_index]*KW)

    return data_map

    
def windprod_Map_sum(data, KW, RELIB, turbine_index, hgt_index):
    import numpy as np
    
    map_rows = np.shape(data.speed)[2]
    map_cols = np.shape(data.speed)[3]
    
    data_map = np.zeros((map_rows, map_cols))
    
    for i in range(0,map_rows):
        for j in range(0,map_cols):
            
            data_map[i,j] = np.sum(RELIB[(np.round(data.speed[:,hgt_index,i,j],2)*100).astype(int),turbine_index]*KW)

    return data_map

def plot_Map(data, to_plot, title, cb_label):
    # flat vectors are expected
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
    plt.close('all')
    fig = plt.figure(999)
    fig.set_size_inches(12,10)
    
    # Basemap latlon init 
    
    
    lon_init = 78      # center lon
    lan_init = 23      # center lan
    lllat = 7.8           # lower left lat 
    lllon = 69         # Lower left lon
    urlat = 32       # upper right lat   
    urlon = 89          # upper right lon
    parallels = np.arange(0.,90,2)
    meridians = np.arange(0,360,5)
    
    m = Basemap(projection='stere',lon_0 = lon_init, lat_0 = lan_init, lat_ts=90,\
                 llcrnrlat=lllat,urcrnrlat=urlat,\
                 llcrnrlon=lllon,urcrnrlon=urlon,\
                 rsphere=6371200.,resolution='i',area_thresh=10000)
    m.drawmapboundary(fill_color='aqua')
    m.drawcoastlines()
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=16)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=16)
    plt.title(str(title), fontsize = 16)
    plt.xlabel('Longitude', fontsize = 14, labelpad = 30)
    plt.ylabel('Latitude', fontsize = 14, labelpad = 60)
    ax = m.scatter(data.lon,data.lat, c = to_plot, latlon = True, s = 38)
    cb = plt.colorbar(ax)  
    cb.set_label(str(cb_label), fontsize = 16, labelpad = 10)
    
def VRE_var_t():
    import json
    from shapely.geometry import shape, Point
    # depending on your version, use: from shapely.geometry import shape, Point

    # load GeoJSON file containing sectors
    with open('Indian.json') as f:
        js = json.load(f)

    # construct point based on lon/lat returned by geocoder
    point = Point(-122.7924463, 45.4519896)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            print(sucesss)
      
    
