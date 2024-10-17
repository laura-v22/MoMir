import pandas as pd
import numpy as np
from datetime import datetime
from pyproj import CRS
from pyproj import Transformer

#=================
#    LEVELLING
#=================
benchmarks = pd.read_csv('csv_data/levelling_2020.csv', index_col='id')


# it's better if the index is strings, not integers,
# despite the fact that benchmark names are integers
# (one reason is that parquet doesn't work otherwise)
benchmarks.index = benchmarks.index.map(str)


# Coordinate conversion for compatibility with Scattermapbox
origin_crs = CRS.from_string('+proj=utm +zone=32 +north')
origin_epsg = origin_crs.to_epsg()
destination_epsg = 4326 # required by Scattermapbox
origin_string = 'EPSG:{}'.format(origin_epsg)
destination_string = 'EPSG:{}'.format(destination_epsg)

transformer = Transformer.from_crs(
    origin_string,
    destination_string,
    always_xy=True
)

utm_longitudes = benchmarks['x_UTM32n'].values
utm_latitudes = benchmarks['y_UTM32n'].values

latitudes = []
longitudes = []

for lat, lon in zip(utm_latitudes, utm_longitudes):
    transformed = transformer.transform(lon, lat)
    longitudes.append(transformed[0])
    latitudes.append(transformed[1])

benchmarks['lat'] = latitudes
benchmarks['lon'] = longitudes

# Separation in two DataFrames: one for info regarding the benchmarks
# (including position), the other with levelling DataFrames

# benchmark_info has ids as index
benchmark_info = benchmarks[['lat', 'lon', 'rel']]

# benchmark_data has dates as index
datenames = ['mag-93', 'ott-03', 'ott-04', 'lug-05', 'giu-06', 'lug-08', 'lug-10', 'lug-12', 'giu-14', 'giu-16', 'giu-18', 'giu-20']
dates = ['1993-05','2003-10','2004-10','2005-07','2006-06','2008-07','2010-07','2012-07','2014-06','2016-06','2018-06','2020-06']
dt_dates = [datetime.strptime(t, '%Y-%m') for t in dates]

benchmark_data = benchmarks[datenames]
benchmark_data = benchmark_data.transpose()
benchmark_data.index = dt_dates

benchmark_info.to_parquet('parquet_data/levelling_info')
benchmark_data.to_parquet('parquet_data/levelling_data')



#=================
#    SATELLITE
#=================

def readSatelliteData(path, sat, datatype):
    """
    Reads satellite data from a file and returns
    two DataFrames, one containing metadata and
    one containing measurements.
    *sat* can be:
        - ers
        - env
        - sen
        - csk
    *datatype* can be:
        - asc
        - des
        - ver
        - hor
    """
    df = pd.read_csv(path)
    if datatype == 'asc' or datatype == 'des':
        df = df.set_index('ID')
    # rename index entries prepending satellite and datatype
    df = df.rename((sat + '-' + datatype + '-{}').format)
    if datatype == 'asc' or datatype == 'des':
        df_info = df[['LAT', 'LON', 'HEIGHT', 'COHER', 'VEL']].copy()
    elif datatype == 'ver':
        df_info = df[['LAT', 'LON', 'VEL']].copy()
    df_info.loc[:,'TYPE'] = datatype

    if datatype == 'ver':
        cols_to_skip = 3
    else:
        cols_to_skip = 16

    df_data = df.iloc[:, cols_to_skip:].copy().transpose()
    dates = df_data.index
    dt_dates = [datetime.strptime(d, 'D%Y%m%d') for d in dates]
    df_data.index = dt_dates

    return df_info, df_data

#---------------
#    ERS LOS
#---------------
ers_asc_info, ers_asc_data = readSatelliteData('csv_data/sat_los/ERS_ASC.csv', 'ers', 'asc')
ers_des_info, ers_des_data = readSatelliteData('csv_data/sat_los/ERS_DESC.csv', 'ers', 'des')

ers_info = pd.concat([ers_asc_info, ers_des_info], axis=0)

ers_info.to_parquet('parquet_data/sat_los/ers_info')
ers_asc_data.to_parquet('parquet_data/sat_los/ers_asc')
ers_des_data.to_parquet('parquet_data/sat_los/ers_des')


#-------------------
#    ENVISAT LOS
#-------------------
env_asc_info, env_asc_data = readSatelliteData('csv_data/sat_los/ENV_ASC.csv', 'env', 'asc')
env_des_info, env_des_data = readSatelliteData('csv_data/sat_los/ENV_DESC.csv', 'env', 'des')

env_info = pd.concat([env_asc_info, env_des_info], axis=0)

env_info.to_parquet('parquet_data/sat_los/env_info')
env_asc_data.to_parquet('parquet_data/sat_los/env_asc')
env_des_data.to_parquet('parquet_data/sat_los/env_des')



#--------------------
#    SENTINEL LOS
#--------------------
sen_asc_info, sen_asc_data = readSatelliteData('csv_data/sat_los/SENT_ASC.csv', 'sen', 'asc')
sen_des_info, sen_des_data = readSatelliteData('csv_data/sat_los/SENT_DESC.csv', 'sen', 'des')

sen_info = pd.concat([sen_asc_info, sen_des_info], axis=0)

sen_info.to_parquet('parquet_data/sat_los/sen_info')
sen_asc_data.to_parquet('parquet_data/sat_los/sen_asc')
sen_des_data.to_parquet('parquet_data/sat_los/sen_des')


#------------------------
#    COSMO-SKYMED LOS
#------------------------
csk_asc_info, csk_asc_data = readSatelliteData('csv_data/sat_los/CSK_ASC.csv', 'csk', 'asc')
csk_des_info, csk_des_data = readSatelliteData('csv_data/sat_los/CSK_DESC.csv', 'csk', 'des')

csk_info = pd.concat([csk_asc_info, csk_des_info], axis=0)

csk_info.to_parquet('parquet_data/sat_los/csk_info')
csk_asc_data.to_parquet('parquet_data/sat_los/csk_asc')
csk_des_data.to_parquet('parquet_data/sat_los/csk_des')



#---------------------------------------------------

#---------------
#    ERS VER
#---------------
ers_ver_info, ers_ver_data = readSatelliteData('csv_data/sat_ver/ERS_up.csv', 'ers', 'ver')

ers_ver_info.to_parquet('parquet_data/sat_ver/ers_ver_info')
ers_ver_data.to_parquet('parquet_data/sat_ver/ers_ver')


#-------------------
#    ENVISAT VER
#-------------------
env_ver_info, env_ver_data = readSatelliteData('csv_data/sat_ver/ENV_up.csv', 'env', 'ver')

env_ver_info.to_parquet('parquet_data/sat_ver/env_ver_info')
env_ver_data.to_parquet('parquet_data/sat_ver/env_ver')


#--------------------
#    SENTINEL VER
#--------------------
sen_ver_info, sen_ver_data = readSatelliteData('csv_data/sat_ver/SEN_up.csv', 'sen', 'ver')

sen_ver_info.to_parquet('parquet_data/sat_ver/sen_ver_info')
sen_ver_data.to_parquet('parquet_data/sat_ver/sen_ver')


#------------------------
#    COSMO-SKYMED VER
#------------------------
csk_ver_info, csk_ver_data = readSatelliteData('csv_data/sat_ver/CSK_up.csv', 'csk', 'ver')

csk_ver_info.to_parquet('parquet_data/sat_ver/csk_ver_info')
csk_ver_data.to_parquet('parquet_data/sat_ver/csk_ver')















