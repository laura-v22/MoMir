import pandas as pd

#======================
#    LEVELLING DATA
#======================
S_LEVELLING_INFO = pd.read_parquet('data/square/parquet_data/levelling_info')
S_LEVELLING_DATA = pd.read_parquet('data/square/parquet_data/levelling_data')


#======================
#    SATELLITE DATA
#======================
ERS_LOS_INFO = pd.read_parquet('data/square/parquet_data/sat_los/ers_info')
ERS_ASC = pd.read_parquet('data/square/parquet_data/sat_los/ers_asc')
ERS_DES = pd.read_parquet('data/square/parquet_data/sat_los/ers_des')
ERS_VER_INFO = pd.read_parquet('data/square/parquet_data/sat_ver/ers_ver_info')
ERS_VER = pd.read_parquet('data/square/parquet_data/sat_ver/ers_ver')

ENV_LOS_INFO = pd.read_parquet('data/square/parquet_data/sat_los/env_info')
ENV_ASC = pd.read_parquet('data/square/parquet_data/sat_los/env_asc')
ENV_DES = pd.read_parquet('data/square/parquet_data/sat_los/env_des')
ENV_VER_INFO = pd.read_parquet('data/square/parquet_data/sat_ver/env_ver_info')
ENV_VER = pd.read_parquet('data/square/parquet_data/sat_ver/env_ver')

SEN_LOS_INFO = pd.read_parquet('data/square/parquet_data/sat_los/sen_info')
SEN_ASC = pd.read_parquet('data/square/parquet_data/sat_los/sen_asc')
SEN_DES = pd.read_parquet('data/square/parquet_data/sat_los/sen_des')
SEN_VER_INFO = pd.read_parquet('data/square/parquet_data/sat_ver/sen_ver_info')
SEN_VER = pd.read_parquet('data/square/parquet_data/sat_ver/sen_ver')

CSK_LOS_INFO = pd.read_parquet('data/square/parquet_data/sat_los/csk_info')
CSK_ASC = pd.read_parquet('data/square/parquet_data/sat_los/csk_asc')
CSK_DES = pd.read_parquet('data/square/parquet_data/sat_los/csk_des')
CSK_VER_INFO = pd.read_parquet('data/square/parquet_data/sat_ver/csk_ver_info')
CSK_VER = pd.read_parquet('data/square/parquet_data/sat_ver/csk_ver')

