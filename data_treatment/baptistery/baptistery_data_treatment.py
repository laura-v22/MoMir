# package imports
import numpy as np
import pandas as pd

#===================
#    SENSOR DATA
#===================

# PRISMS
def readPrismData():
    # read info about prisms for column indices
    prisms = np.loadtxt(
        'csv_data/prisms.csv',
        delimiter='\t',
        dtype='object',
        max_rows=1
    )
    prisms = [el for el in prisms if el!='']
    directions = ['x', 'y', 'z']*len(prisms)
    tmp = []
    for p in prisms:
        tmp += [p]*3
    prism_multiindex = np.array([tmp, directions]).transpose()

    # read prism data
    tmp = pd.read_csv(
        'csv_data/prisms.csv',
        delimiter = "\t",
        index_col= 0,
        skiprows=1,
        parse_dates=True
    )

    # Format prism DataFrame with MultiIndex
    prism_data = pd.DataFrame(
        tmp.values,
        index=tmp.index,
        columns=prism_multiindex
    )
    prism_data.columns = pd.MultiIndex.from_tuples(prism_data.columns)

    return prism_data


# LEVELLING
def readLevellingData():
    levelling_data = pd.read_csv(
        'csv_data/levelling.csv',
        delimiter='\t',
        index_col='date',
        parse_dates=True
    )
    return levelling_data


# EXTENSIMETERS
def readExtensimeterData():
    # read extensimeter data (position and temperature) in a temporary
    # DataFrame because there are two separate columns for date and time
    tmp = pd.read_csv(
        'csv_data/extensimeters.csv',
        delimiter=';',
        header=[0,1]
    )

    # create a new DataFrame with a single index DateTime column
    cols_to_join = tmp.columns[:2]
    dt_index = [
        tmp[cols_to_join[0]].iloc[i] + ' ' + tmp[cols_to_join[1]].iloc[i]
        for i in range(len(tmp.index))
    ]
    extensimeter_data = pd.DataFrame(
        tmp[tmp.columns[2:]].values,
        index=dt_index,
        columns=tmp.columns[2:]
    )
    extensimeter_data.index = pd.to_datetime(extensimeter_data.index)

    # removes measurements if temperature == 0°C
    # (because we think they are outliers)
    extensimeter_data = extensimeter_data.replace(0.0, np.nan).dropna().copy()

    return extensimeter_data

PRISMS = readPrismData()
LEVELLING = readLevellingData()
EXTENSIMETERS = readExtensimeterData()

PRISMS.to_parquet('parquet_data/prisms')
LEVELLING.to_parquet('parquet_data/levelling')
EXTENSIMETERS.to_parquet('parquet_data/extensimeters')


#=======================
#    SENSOR POSITION
#=======================
def readSensorPositions():
    # prism positions
    prism_pos = pd.read_csv(
        'csv_data/positions/prism_angles.csv',
        index_col=0,
        names=['angle', 'radius', 'z']
    )
    prism_pos['type'] = ['prism']*len(prism_pos)

    # levelling benchmark positions
    levelling_pos = pd.read_csv(
        'csv_data/positions/levelling_angles.csv',
        index_col=0,
        names=['angle','radius', 'z']
    )
    levelling_pos['type'] = ['level']*len(levelling_pos)

    # extensimeter positions
    extensimeter_pos = pd.read_csv(
        'csv_data/positions/extensimeter_angles.csv',
        index_col=0,
        names=['angle','radius', 'z']
    )
    extensimeter_pos['type'] = ['crack']*len(extensimeter_pos)

    # single DataFrame with all instrument positions
    positions = pd.concat([prism_pos, levelling_pos, extensimeter_pos], axis=0)

    return prism_pos, levelling_pos, extensimeter_pos, positions

PRISM_POS, LEVELLING_POS, EXTENSIMETER_POS, POSITIONS = readSensorPositions()

#=======================
#    3D PRISMS CONNECTIVITY MATRIX
#=======================
conn=pd.read_csv('csv_data/conn_matrix.csv',delimiter=';',header=None,dtype='str')
conn.to_parquet('parquet_data/connmat')



PRISM_POS.to_parquet('parquet_data/positions/prism_angles')
LEVELLING_POS.to_parquet('parquet_data/positions/levelling_angles')
EXTENSIMETER_POS.to_parquet('parquet_data/positions/extensimeter_angles')
POSITIONS.to_parquet('parquet_data/positions/positions')


