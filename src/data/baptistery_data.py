# package imports
import pandas as pd

#===================
#    SENSOR DATA
#===================
B_PRISMS = pd.read_parquet('data/baptistery/parquet_data/prisms')
B_LEVELLING = pd.read_parquet('data/baptistery/parquet_data/levelling')
B_EXTENSIMETERS = pd.read_parquet('data/baptistery/parquet_data/extensimeters')

#=====================
#    POSITION DATA
#=====================
B_PRISM_POS = pd.read_parquet('data/baptistery/parquet_data/positions/prism_angles')
B_LEVELLING_POS = pd.read_parquet('data/baptistery/parquet_data/positions/levelling_angles')
B_EXTENSIMETER_POS = pd.read_parquet('data/baptistery/parquet_data/positions/extensimeter_angles')
B_POSITIONS = pd.read_parquet('data/baptistery/parquet_data/positions/positions')

#=====================
#  3D DATA
#=====================
CONNMAT = pd.read_parquet('data/baptistery/parquet_data/connmat')
