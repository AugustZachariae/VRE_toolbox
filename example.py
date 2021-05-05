# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:27:21 2020

@author: August Zachariae, Advisor Danish Energy Agency
@co-author: Prashant Bhamu, Assistant Director, Central Electricity Authority
"""
#%% import of basic functions, always run first. 
#Only needs to run once, but running multiple times does not affect code

import xarray as xr
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import spatial as ss
from scipy import interpolate
import cdsapi
import os
import pandas as pd
from datetime import datetime
os.environ['PROJ_LIB'] = r'C:\Users\Bruger\Anaconda3\pkgs\proj4-5.2.0-h6538335_1006\Library\share'
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from netCDF4 import Dataset
from pyproj import Proj

os.chdir(r'C:\Users\Bruger\Documents\VRE_Toolbox')
from VRE_toolbox_functions import *

filenameRELIB = 'RE_LIB_1.csv'
RELIB, RELIBheader = readcsv(filenameRELIB, ',')
import json
with open('Indian_states.json') as f:
    js = json.load(f)
import geopandas as gpd
from shapely.geometry import shape, Point
from shapely.geometry.polygon import Polygon    
Bihar=Polygon(tuple(js['features'][4]['geometry']['coordinates'][1])[0])
Andra_Pradesh=Polygon(tuple(js['features'][1]['geometry']['coordinates'][31])[0])
Arunachal_pradesh=Polygon(tuple(js['features'][2]['geometry']['coordinates'][0]))
Assam = Polygon(tuple(js['features'][3]['geometry']['coordinates'][2])[0])
Chattisgarth=Polygon(tuple(js['features'][6]['geometry']['coordinates'][0]))
Goa=Polygon(tuple(js['features'][10]['geometry']['coordinates'][3])[0])
Gujaret=Polygon(tuple(js['features'][11]['geometry']['coordinates'][178])[0])
Haryana=Polygon(tuple(js['features'][12]['geometry']['coordinates'][0]))
Jammu_Kashmir=Polygon(tuple(js['features'][14]['geometry']['coordinates'][0]))
Jharkhand=Polygon(tuple(js['features'][15]['geometry']['coordinates'][0]))
Karnataka=Polygon(tuple(js['features'][16]['geometry']['coordinates'][23])[0])
Kerala=Polygon(tuple(js['features'][17]['geometry']['coordinates'][44])[0])
Madhya_Pradesh=Polygon(tuple(js['features'][19]['geometry']['coordinates'][0]))
Maharashtra=Polygon(tuple(js['features'][20]['geometry']['coordinates'][18])[0])
Manipur=Polygon(tuple(js['features'][21]['geometry']['coordinates'][0]))
Meghalaya=Polygon(tuple(js['features'][22]['geometry']['coordinates'][0]))
Mizoram=Polygon(tuple(js['features'][23]['geometry']['coordinates'][0]))
Nagaland=Polygon(tuple(js['features'][24]['geometry']['coordinates'][0]))
Orissa=Polygon(tuple(js['features'][25]['geometry']['coordinates'][50])[0])
Punjab=Polygon(tuple(js['features'][27]['geometry']['coordinates'][0]))
Rajasthan=Polygon(tuple(js['features'][28]['geometry']['coordinates'][0]))
Sikkim=Polygon(tuple(js['features'][29]['geometry']['coordinates'][0]))
Tamil_Nadu=Polygon(tuple(js['features'][30]['geometry']['coordinates'][54][0]))
Tripura=Polygon(tuple(js['features'][31]['geometry']['coordinates'][0]))
Uttar_Pradesh=Polygon(tuple(js['features'][32]['geometry']['coordinates'][0]))
Uttaranchal=Polygon(tuple(js['features'][33]['geometry']['coordinates'][0]))
West_Bengal=Polygon(tuple(js['features'][34]['geometry']['coordinates'][119][0]))

#Union terrotories

Chandigarh=Polygon(tuple(js['features'][5]['geometry']['coordinates'][0]))
Dadra_Nagar_Haveli=Polygon(tuple(js['features'][7]['geometry']['coordinates'][0]))
Delhi=Polygon(tuple(js['features'][9]['geometry']['coordinates'][0]))
Himachal_Pradesh=Polygon(tuple(js['features'][13]['geometry']['coordinates'][0]))
Lakshadweep=Polygon(tuple(js['features'][18]['geometry']['coordinates'][23])[0])

Wind_states=[Andra_Pradesh,Gujaret,Karnataka,Kerala,Madhya_Pradesh,Maharashtra,Rajasthan,Tamil_Nadu]
Wind_state_names=['Andra_Pradesh','Gujaret','Karnataka','Kerala','Madhya_Pradesh','Maharashtra','Rajasthan','Tamil_Nadu']
T_h=[27,29,30,39,42,44,47,52,66,66,66,80,80,90,90,90,100,100,110,112,112,164]

OffshoreAreas=gpd.read_file('Polygon.shp')
GujaretOS1=OffshoreAreas.iloc[1,0]
GujaretOS2=OffshoreAreas.iloc[0,0]
Tamil_NaduOS1=OffshoreAreas.iloc[3,0]
Tamil_NaduOS2=OffshoreAreas.iloc[2,0]
OS_areas=[GujaretOS1,GujaretOS2,Tamil_NaduOS1,Tamil_NaduOS2]
OS_areas_names=['GujaretOS1','GujaretOS2','Tamil_NaduOS1','Tamil_NaduOS2']
#%% Import of data into python
# import data into script 
# change filename to whatever you named the data
# The file needs to be placed within the folder in which the python files are located 
filenameERA = 'ERA5_IN_Wind_2015.nc'
E2020 = getNCData(filenameERA, "ERA5")


#%%Wind settings Rajastan
V100_index = 66
#hgt_index 0=10 meter and 1=100 meter
hgt_index = 1
kw=1

#%%Wind settings Rajastan
V100_index = 25
#hgt_index 0=10 meter and 1=100 meter
hgt_index = 1
kw=1
#%%an overview of functions to use

#map_subset(data)
#wind_var_t
#plot_map
#%%Wind settings check RELIBHEADER
V100_index = 95
hgt_index = 1
kw=1
#%%
#avgmap = windspeed_map_avg(E2020, hgt_index)
#%%
summap = windprod_Map_sum(E2020, kw, RELIB, V100_index, hgt_index)
plot_Map(E2020,summap , 'Average annual production 100 m altitude', 'MWh')

#%%
subdata= map_subset(E2020,Andra_Pradesh)
avgmap = windspeed_map_avg(subdata, hgt_index)
plot_Map(E2020,avgmap , 'submap Average wind speed 2020_08 (100 m altitude)', 'm/s')
#%%
summap = windprod_Map_sum(subdata, kw, RELIB, V100_index, hgt_index)
plot_Map(subdata,summap , 'sub V100, average production 2020_08', 'Production [Mwh]')
#%%
#%%Wind settings Rajastan test 95-115
V100_index = 107
#hgt_index 0=10 meter and 1=100 meter
hgt_index = 1
kw=1
CF=wind_var_t(subdata,RELIB,V100_index,65,95, hgt_index,110)
import matplotlib.pyplot as pp
pp.plot(CF)
pp.show()
to_clipboard(CF, decimal=".")

#%%
qt_list=[95,90,85,80,75,70,65,60,55,50,45,40,35,30,25,20,15,10,5,0]
CF=np.empty_like(E2020.datetime)
counter=0

for state in Wind_states:
    counter=counter+1
    writer = pd.ExcelWriter(Wind_state_names[counter-1]+'.xlsx', engine='xlsxwriter')
    subdata= map_subset(E2020,state)
    CF=np.empty_like(subdata.datetime)
    CF_QT=[]
    for qt in qt_list:
        CF=np.empty_like(subdata.datetime)
        CF[:]=qt
        for turbine in range(95,116):
            print(turbine)
            V100_index = turbine
            #hgt_index 0=10 meter and 1=100 meter
            hgt_index = 1
            kw=1
            CF=np.dstack((CF,wind_var_t(subdata,RELIB,V100_index,qt,100, hgt_index,T_h[counter-1])))
        
        CF_QT.append(CF[0])
    CF_QT=np.vstack(CF_QT)
    df = pd.DataFrame(CF_QT)
#        df.to_excel(excel_writer = "C:/Users/Bruger/Desktop/state_"+str(int(counter))+str(int(qt))".xlsx")
    df.to_excel(writer, str(int(qt))+'lower qt')
    writer.save()    
    
#%%
qt_list=[0]
CF=np.empty_like(E2020.datetime)
counter=0

for state in OS_areas:
    counter=counter+1
    writer = pd.ExcelWriter(OS_areas_names[counter-1]+'.xlsx', engine='xlsxwriter')
    subdata= map_subset(E2020,state)
    CF=np.empty_like(subdata.datetime)
    CF_QT=[]
    for qt in qt_list:
        CF=np.empty_like(subdata.datetime)
        CF[:]=qt
        for turbine in range(95,116):
            print(turbine)
            V100_index = turbine
            #hgt_index 0=10 meter and 1=100 meter
            hgt_index = 1
            kw=1
            CF=np.dstack((CF,wind_var_t(subdata,RELIB,V100_index,qt,100, hgt_index,T_h[counter-1])))
        
        CF_QT.append(CF[0])
    CF_QT=np.vstack(CF_QT)
    df = pd.DataFrame(CF_QT)
#        df.to_excel(excel_writer = "C:/Users/Bruger/Desktop/state_"+str(int(counter))+str(int(qt))".xlsx")
    df.to_excel(writer, str(int(qt))+'lower qt')
    writer.save()    