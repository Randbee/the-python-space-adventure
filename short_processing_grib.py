#!/usr/bin/python

import pygrib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.basemap import shiftgrid
import os
import re
import datetime


data = datetime.datetime.now().isoformat()
data_split = data.split('T')
data = data_split[0]
### type of data used on fow download
data2 = data.replace("-", "")


input_path = "/home/randbee/the-python-space-adventure/pollutants/data"
output_path = "/home/randbee/the-python-space-adventure/pollutants/output"
os.chdir(input_path)
grib='z_cams_c_ecmf_20180918000000_prod_fc_sfc_024_pm1.grib' # Set the file name of your input GRIB file
grbs=pygrib.open(grib)
for grb in grbs: grb
### analysing data ####

# list of contaminator

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def normalization(x):
    "normalization of the values of a gribfile. grb.values are returned normalized "
    os.chdir(input_path)
    grbs = pygrib.open(x)
    for grb in grbs: grb
    grb = grbs.select()[0]
    data = grb.values
    data_min = grb.minimum
    data_max = grb.maximum
    norm = (data - data_min)/(data_max - data_min) * 100
    return norm


def polloutants(x):
    "open grib for pm, nox, uvbed"
    os.chdir(input_path)
    grbs = pygrib.open(x)
    grb = grbs.select()[0]
    data = grb.values
    return data


def for_ozone(x):
    "open ozone grib"
    os.chdir(input_path)
    grbs = pygrib.open(x)
    grb = grbs.select()[59]
    data = grb.values
    return data


def norm_ozone(x):
    "normalization of the values of ozone gribfile. grb.values are returned normalized "
    os.chdir(output_path)
    grbs = pygrib.open(x)
    grb = grbs.select()[0]
    data = grb.values
    data_min = grb.minimum
    data_max = grb.maximum
    norm = (data - data_min)/(data_max - data_min) * 100
    return norm

# list of the our available on the analysis
# list_hours = ['sfc_000', 'sfc_001', 'sfc_002','sfc_003', 'sfc_004', 'sfc_005',
#             'sfc_006', 'sfc_007', 'sfc_008', 'sfc_009', 'sfc_010', 'sfc_011',
#             'sfc_012', 'sfc_013', 'sfc_014', 'sfc_015', 'sfc_016', 'sfc_017',
#             'sfc_018', 'sfc_019','sfc_020', 'sfc_021', 'sfc_022', 'sfc_023' ]

list_hours = ['sfc_024', 'sfc_025', 'sfc_026','sfc_027', 'sfc_028', 'sfc_029',
            'sfc_030', 'sfc_031', 'sfc_032', 'sfc_033', 'sfc_034', 'sfc_035',
            'sfc_036', 'sfc_037', 'sfc_038', 'sfc_039', 'sfc_040', 'sfc_041',
            'sfc_042', 'sfc_043','sfc_044', 'sfc_045', 'sfc_046', 'sfc_047' ]



griblist = os.listdir(input_path)


todelete_list = [ f for f in os.listdir(output_path) if f.endswith(".grib") ]

for g in todelete_list:
    os.remove(os.path.join(output_path, g))


for hours in list_hours:
    data_sum0 = np.zeros((451, 900))
    data_pm0 = np.zeros((451, 900))
    data_nox0 = np.zeros((451, 900))
    data_uv0 = np.zeros((451, 900))
    for grib_file in griblist:
        if hours in grib_file:
            data = normalization(grib_file)
            data_sum0 = data_sum0 + data
            # print grib_file
            if 'pm' in grib_file:
                data = polloutants(grib_file)
                data_pm0 = data_pm0 + data
                data_pm0 = data_pm0
                # print grib_file
            if 'no' in grib_file:
                data = polloutants(grib_file)
                data_nox0 = data_nox0 + data
                # print grib_file
            if 'uv' in grib_file:
                data = polloutants(grib_file)
                data_uv0 = data / 0.025 #have back uv index
                # print grib_file

    # text, hour =hours.split('_0')
    text, hour =hours.split('_0')
    hour =int(hour)
    const = 24
    corr_hour = hour - const
    # print corr_hour
    if corr_hour < 10:
        hour = '0' + str(corr_hour)
    else:
        hour = str(corr_hour)
    os.chdir(output_path)
    ## skin ageing ##



    ## particular matter ##
    min_value_pm = data_pm0.min()
    max_value_pm = data_pm0.max()
    grb['values'] = (data_pm0 - min_value_pm) / (max_value_pm - min_value_pm)
    pm = 'pm_'+ hour + '.grib'
    print pm
    grbout = open(pm,'wb')
    msg = grb.tostring()
    grbout.write(msg)
    grbout.close()


    ## ultra violet index ##
    min_value_uv = data_uv0.min()
    max_value_uv = data_uv0.max()
    grb['values'] = (data_uv0 - min_value_uv) / (max_value_uv - min_value_uv)
    uvi = 'uvi_'+ hour + '.grib'
    print uvi
    grbout = open(uvi,'wb')
    msg = grb.tostring()
    grbout.write(msg)
    grbout.close()

    ## nox ##
    min_value_nox = data_nox0.min()
    max_value_nox = data_nox0.max()
    grb['values'] = (data_nox0 - min_value_nox) / (max_value_nox - min_value_nox)
    nox = 'nox_'+ hour + '.grib'
    print nox
    grbout = open(nox,'wb')
    msg = grb.tostring()
    grbout.write(msg)
    grbout.close()

# o3_hour = ['ml_000', 'ml_003', 'ml_006',  'ml_009',
#             'ml_012', 'ml_015', 'ml_018', 'ml_021' ]
#
o3_hour = ['ml_024', 'ml_027', 'ml_030',  'ml_033',
            'ml_036', 'ml_039', 'ml_042', 'ml_045' ]

griblist = os.listdir(input_path)
for hours in o3_hour:
    data_sum0 = np.zeros((451, 900))
    data_o3_0 = np.zeros((451, 900))
    # print hours
    for grib_file in griblist:
        if hours in grib_file:
            data = for_ozone(grib_file)
            data_o3_0 = data
    text, hour =hours.split('_0')
    hour =int(hour)
    const = 24
    corr_hour = hour - const
    # print corr_hour
    if corr_hour < 10:
        hour = '0' + str(corr_hour)
    else:
        hour = str(corr_hour)
    os.chdir(output_path)
    ## ozone ##
    ########## UNIT value for ozone, kg/kg  ##########
    ## 1000 from kg to g
    ## 1000 grom kg to mg
    min_value_o3 = data_o3_0.min()
    max_value_o3 = data_o3_0.max()
    grb['values'] = (data_o3_0 - min_value_o3) / (max_value_o3 - min_value_o3)
    o3 = 'o3_'+ hour + '.grib'
    print o3
    grbout = open(o3,'wb')
    msg = grb.tostring()
    grbout.write(msg)
    grbout.close()
