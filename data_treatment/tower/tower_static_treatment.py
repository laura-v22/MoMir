import pandas as pd
import glob

#============================
#    TOWER STATIC SENSORS
#============================

filelist = glob.glob('csv_data/static/*_csvreg')

time_map = {'Yyyy':'year','Mm':'month','Dd':'day', 'Hh':'hour','Mn':'minute'}

for f in filelist:
    df = pd.read_csv(
    f,
    delimiter=';',
    index_col=False,
    usecols=['Yyyy', 'Mm', 'Dd', 'Hh', 'Mn', 'UI', 'TAG'],
)
    df = df.rename(columns=time_map)
    df['datetime'] = pd.to_datetime(df[list(time_map.values())])

    years = df['year'].unique()
    sensors = df['TAG'].unique()

    for y in years:
        yearly_df = pd.DataFrame()
        tmp_df = df[df['year'] == y]
        for s in sensors:
            tmp_df_s = tmp_df[tmp_df['TAG'] == s]
            tmp_df_s = tmp_df_s.set_index('datetime')
            tmp_df_s = tmp_df_s[~tmp_df_s.index.duplicated(keep='first')]
            sensor_df = pd.DataFrame({s: tmp_df_s['UI'].values}, index=tmp_df_s.index)
            yearly_df = yearly_df.join(sensor_df, how='outer')
        yearly_df.to_parquet('parquet_data/static/h_'+str(y))
        yearly_df.resample('1D').mean().to_parquet('parquet_data/static/d_'+str(y))
        yearly_df.resample('1W').mean().to_parquet('parquet_data/static/w_'+str(y))
        yearly_df.resample('1M').mean().to_parquet('parquet_data/static/m_'+str(y))

with open('parquet_data/static/all_sensors.txt', 'w') as sensors_file:
    sensors_file.write(','.join(list(sensors)))
