import pandas as pd
import glob

#=================================
#    LEVELLING BY CAPRARO DATA
#=================================
T_CAPRARO_DATA = pd.read_parquet('data/tower/parquet_data/capraro/tower_levelling')
T_CAPRARO_BENCHMARKS = pd.read_parquet('data/tower/parquet_data/capraro/tower_benchmark_positions')

#=====================================
#    STABILIZATION BENCHMARKS DATA
#=====================================
T_STABIL_COORDS = pd.read_parquet('data/tower/parquet_data/stabil_bench_coords')
T_STABIL_DISP = pd.read_parquet('data/tower/parquet_data/stabil_bench_disp')


#=====================================
#    STATIC DATA
#====================================
file_pattern ='data/tower/parquet_data/static/*'

# List all Parquet files in the directory using glob
for filepath in glob.glob(file_pattern):
    # Extract filename from the full path
    filename = filepath.split('\\')[-1]
    
    # Generate the name for the DataFrame
    if not filename.endswith('.txt'):
        df_name = filename.replace('.parquet', '').upper()
    
    # Create the DataFrame by reading the Parquet file
        dataframe = pd.read_parquet(filepath)
    
    # Assign the DataFrame to a variable name in the global namespace
        globals()[df_name] = dataframe