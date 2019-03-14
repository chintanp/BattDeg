import pandas as pd
import numpy as np
import datetime
import os
import re
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import seaborn as sns

def PL_samples_file_reader(data_dir, file_name_format, ignore_file_indices):
    """
    This function reads in the data for PL Samples experiment and returns a 
    nice dataframe with cycles in ascending order. 
    
    Args: 
        data_dir (string): This is the absolute path to the data directory. 
        file_name_format (string): Format of the filename, used to deduce other files.
        ignore_file_indices (list, int): This list of ints tells which to ignore.
        
    Returns:
        The complete test data in a dataframe with extra column for capacity in Ah.
    """
    
    # Raise an exception if the type of the inputs is not correct
    if not isinstance(data_dir, str):
        raise TypeError('data_dir is not of type string')
    
    if not isinstance(file_name_format, str):
        raise TypeError('file_name_format is not of type string')
  
    if not isinstance(ignore_file_indices, list):
        raise TypeError("ignore_file_indices should be a list")

    for i in range(len(ignore_file_indices)):
        if not isinstance(ignore_file_indices[i], int):
            raise TypeError("""ignore_file_indices elements should be 
            of type integer""")
    
    if not os.path.exists(join(data_dir, file_name_format)):
        raise FileNotFoundError("File {} not found in the location {}"
        .format(file_name_format, data_dir))
    
    # get the list of files in the directory
    onlyfiles = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    
    # Extract the experiment name from the file_name_format
    exp_name = file_name_format[0:4]
    
    # Empty dictionary to hold all the dataframe for various files
    dict_files = {}
    
    # Iterate over all the files of certain type and get the file number from them
    for i in range(len(onlyfiles)):
        if exp_name in onlyfiles[i]:
            # Extract the filenumber from the name
            file_number = re.search(exp_name + '\((.+?)\).csv', onlyfiles[i]).group(1)
            # Give a value of dataframe to each key
            dict_files[int(file_number)] = pd.read_csv(join(data_dir, onlyfiles[i]))
    
    # Empty dictionary to hold the ordered dictionaries
    dict_ordered = {}
    # Sort the dictionary based on keys
    for key in sorted(dict_files.keys()):
        dict_ordered[key] = dict_files[key]
    
    # Keys with files to keep, remove the ignore indices from all keys
    wanted_keys = np.array(list(set(dict_ordered.keys()) - set(ignore_file_indices)))
    
    # Remove the ignored dataframes for characterization 
    dict_ord_cycling_data = {k : dict_ordered[k] for k in wanted_keys}
    
    # Concatenate the dataframes to create the total dataframe
    
    df_out = None
    for k in wanted_keys:
        if df_out is None:
            df_next = dict_ord_cycling_data[k]
            df_out = pd.DataFrame(data=None, columns=df_next.columns)
            df_out = pd.concat([df_out, df_next])
        else:
            df_next = dict_ord_cycling_data[k]
            df_next['Cycle'] = df_next['Cycle'] + max(df_out['Cycle'])
            df_next['Time_sec'] = df_next['Time_sec'] + max(df_out['Time_sec'])
            df_next['Charge_Ah'] = df_next['Charge_Ah'] + max(df_out['Charge_Ah'])
            df_next['Discharge_Ah'] = df_next['Discharge_Ah'] + max(df_out['Discharge_Ah'])
            df_out = pd.concat([df_out, df_next])
      
    # Convert the Date_Time from matlab datenum to human readable Date_Time
    df_out['Date_Time_new'] = df_out['Date_Time'].apply(lambda x: datetime.datetime.fromordinal(int(x)) + 
    datetime.timedelta(days=x%1) - datetime.timedelta(days = 366)  )
    
    # Reset the index and drop the old index
    df_out_indexed = df_out.reset_index(drop=True)

    # Proceed further with correcting the capacity 
    df_grouped = df_out_indexed.groupby(['Cycle']).count()
    
    # Get the indices when a cycle starts
    cycle_start_indices = df_grouped['Time_sec'].cumsum()
    
    # Get the charge_Ah per cycle
    df_out_indexed['Charge_cycle_Ah'] = df_out_indexed['Charge_Ah']
    
    for i in range(1, len(cycle_start_indices)):
        a = cycle_start_indices.iloc[i-1]
        b = cycle_start_indices.iloc[i]
        df_out_indexed['Charge_cycle_Ah'].iloc[a:b] = df_out_indexed['Charge_Ah'].iloc[a:b] - max(df_out_indexed['Charge_Ah'].iloc[0:a])

    # Get the discharge_Ah per cycle 
    df_out_indexed['Discharge_cycle_Ah'] = df_out_indexed['Discharge_Ah']
    
    for i in range(1, len(cycle_start_indices)):
        a = cycle_start_indices.iloc[i-1]
        b = cycle_start_indices.iloc[i]
        df_out_indexed['Discharge_cycle_Ah'].iloc[a:b] =  df_out_indexed['Discharge_Ah'].iloc[a:b] - max(df_out_indexed['Discharge_Ah'].iloc[0:a])
        
    # This is the data column we can use for prediction. 
    # This is not totally accurate, as this still has some points that go negative, 
    # due to incorrect discharge_Ah values every few cycles. 
    # But the machine learning algorithm should consider these as outliers and 
    # hopefully get over it. We can come back and correct this. 
    df_out_indexed['Capacity_cycle_Ah'] = df_out_indexed['Charge_cycle_Ah'] - df_out_indexed['Discharge_cycle_Ah']
        
    return df_out_indexed