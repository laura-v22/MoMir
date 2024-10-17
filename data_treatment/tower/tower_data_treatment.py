# package imports
import pandas as pd
import numpy as np
from datetime import datetime

#============================
#    LEVELLING BY CAPRARO
#============================
# first file
lev_tower= pd.read_csv(
    'csv_data/capraro/tower_capraro_lev.csv',
    index_col='48',
    parse_dates=True,
    sep=';'
)

# new measurements
cols = [i for i in range(2,70,4)]
lev_tower_new = pd.read_excel(
    'csv_data/capraro/new_measurements_2021_2023.xlsx',
    usecols=cols,
    skiprows=1
)
lev_tower_new_points = pd.read_excel(
    'csv_data/capraro/new_measurements_2021_2023.xlsx', 
    usecols=[1],
    skiprows=1,
    dtype='string'
)
lev_tower_new.index = lev_tower_new_points.iloc[:,0]
lev_tower_new = (lev_tower_new.T)
lev_tot = pd.concat([lev_tower, lev_tower_new])

# saving
lev_tot.to_parquet('parquet_data/capraro/tower_levelling')


#======================================
#    (CAPRARO) LEVELLING BENCHMARKS
#======================================
# some of the benchmarks which are part of the
# whole square's levelling are also important
# for the Tower. Their coordinates are now 
# referred to the center of the Tower.
## FIX: unify the origin of raw data for levelling

bench_list=[
    14,
    101, 102, 103, 104, 105, 106, 107, 108,
    901, 902, 903, 904, 905, 906, 907, 908, 909,
    910, 911, 912, 913, 914, 915, 920
]

bench_xy = pd.read_csv(
    'csv_data/benchmarks_square_pos.csv', 
    index_col = 'caposaldo', 
    usecols = ['caposaldo','x_coord[m]', 'y_coord[m]', 'type'])

xy = []
for lb in bench_list:
    xy.append(bench_xy.loc[lb])
bench_xy_tower = pd.concat(xy, ignore_index=True, axis=1).transpose()
bench_l = pd.DataFrame(bench_list)
bench_xy_tower = pd.concat([bench_xy_tower, bench_l], axis=1)
bench_xy_tower.columns = ['x','y','type','benchmarks']
bench_xy_tower = bench_xy_tower.set_index('benchmarks')

links = [[102,106], [103,107], [104,108], [105,101]]
center_int_x = [
    (bench_xy_tower.loc[l[0]]['x'] + bench_xy_tower.loc[l[1]]['x'])/2 
    for l in links
]
center_int_y = [
    (bench_xy_tower.loc[l[0]]['y'] + bench_xy_tower.loc[l[1]]['y'])/2
    for l in links
]

def Average(lst):
    return sum(lst)/len(lst)
    
center_int_x = Average(center_int_x)
center_int_y = Average(center_int_y)
bench_xy_tower['x'] = bench_xy_tower['x'] - center_int_x
bench_xy_tower['y'] = bench_xy_tower['y'] - center_int_y


# other benchmarks are only used by Capraro,
# their position is written in another file and loaded here
EI_bench = pd.read_csv(
    'csv_data/capraro/ei_pos.csv', 
    index_col='id',
    usecols=['angle','radius','id','type']
)
EI_bench_coords = pd.DataFrame()
EI_bench_coords['x'] = np.cos(EI_bench['angle']) * EI_bench['radius']
EI_bench_coords['y'] = np.sin(EI_bench['angle']) * EI_bench['radius']
EI_bench_coords['type'] = EI_bench['type']

# the two dataframes are finally concatenated,
# the radial coordinates are recalculated,
# and some cleanup is performed
tower_bench_coord = pd.concat([bench_xy_tower, EI_bench_coords])

# it's better if the index is strings, not integers,
# despite the fact that benchmark names are integers
# (one reason is that parquet doesn't work otherwise)
tower_bench_coord.index = tower_bench_coord.index.map(str)

radius2 = tower_bench_coord['x']**2 + tower_bench_coord['y']**2
radius = [np.sqrt(el) for el in radius2]
change_sign = tower_bench_coord['x'] > 0
radius = radius * ((change_sign*2)-1) #trick to change the sign only if x < 0
tower_bench_coord['radius'] = radius
for b in ['904', 'I6', 'E6']:
    tower_bench_coord.loc[b, 'radius'] = - tower_bench_coord.loc[b, 'radius']

# saving
tower_bench_coord.to_parquet('parquet_data/capraro/tower_benchmark_positions')


#=======================================
#    BENCHMARKS DURING STABILIZATION
#=======================================
stabil_bench = pd.read_csv(
    'csv_data/stabil_pos.csv',
    index_col='id',
    usecols=['angle', 'radius', 'id']
)
stabil_bench_coords = pd.DataFrame()
stabil_bench_coords['x'] = np.cos(stabil_bench['angle']) * stabil_bench['radius']
stabil_bench_coords['y'] = np.sin(stabil_bench['angle']) * stabil_bench['radius']

stabil_disp = pd.read_csv(
    'csv_data/stabil_disp.csv',
    index_col='date'
)
oldindex = stabil_disp.index
newindex = [datetime.strptime(t, '%d/%m/%Y') for t in oldindex]
stabil_disp.index = newindex

# saving
stabil_bench_coords.to_parquet('parquet_data/stabil_bench_coords')
stabil_disp.to_parquet('parquet_data/stabil_bench_disp')