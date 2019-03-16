"""
This module can be used to read cycling data of the CX2 type cells as
a dataframe. It converts cumulative values into individual values for 
each cycle. It also determines net charge of the battery at every datapoint.

"""

import pandas as pd
import numpy as np
import datetime
import os, sys
import re
from os import listdir
from os.path import join
import matplotlib.pyplot as plt
import seaborn as sns


def CX2_sample_file_reader(data_dir, file_name_format, Sheet_Name):
    """
    This function reads in the data for CX2 samples experiment and returns
    a well formatted dataframe with cycles in ascending order.
        
    Args:
    data_dir (string): This is the absolute path to the data directory. 
    file_name_format (string): Format of the filename, used to deduce other files.
        
    Returns:
    The complete test data in a dataframe with extra column for capacity in Ah.
    """
        # Raise an exception if the type of the inputs is not correct
    if not isinstance(data_dir, str):
        raise TypeError('data_dir is not of type string')
    
    if not isinstance(file_name_format, str):
        raise TypeError('file_name_format is not of type string')
        
    if not os.path.exists(data_dir + file_name_format):
        raise FileNotFoundError("File {} not found in the location {}"
        .format(file_name_format, data_dir))
        
    # Get the list of files in the directory
    path = join(data_dir, file_name_format)
    files = listdir(path)
    
    # Extract the experiment name from the file_name_format
    exp_name = file_name_format[0:6]
    
    # Filtering out and reading the excel files in the data directory
    file_names = list(filter(lambda x: x[-5:]=='.xlsx' , files))
    
    # Sorting the file names using the
    # 'file_name_sorting' function.
    sorted_name_list = file_name_sorting(file_names)
    
    # Reading dataframes according to the date of experimentation
    # using 'reading_dataframes' function.
    sorted_df = reading_dataframes(sorted_name_list,Sheet_Name, path)
    
    # Merging all the dataframes and adjusting the cycle index
    # using the 'concat_df' function.
    cycle_data = concat_df(sorted_df)
    
    # Calculating the net capacity of the battery at every datapoint
    # using the function 'capacity'.
    capacity_data = capacity(cycle_data)
    
    # Returns the dataframe with new cycle indices and capacity data.
    return capacity_data

def file_name_sorting(file_name_list):
    """
    This function sorts all the file names according to the date
    on the file name.
    
    Args:
    file_name_list(list): List containing all the file names to be read
    
    Returns:
    A list of file names sorted according to the date on the file name.
    
    """
    fn = pd.DataFrame(data = file_name_list,columns = ['file_name'])
    # Splitting the file name into different columns
    fn['cell_type'],fn['cell_num'],fn['month'],fn['day'],fn['year'] = fn['file_name'].str.split('_', 4).str
    fn['year'], fn['ext'] = fn['year'].str.split('.',1).str
    # Converting the split strings into integers for further formatting
    fn.month = fn.month.astype(int)
    fn.day = fn.day.astype(int)
    fn.year = fn.year.astype(int)
    fn['year'].replace(11,2011,inplace=True)
    fn['year'].replace(12,2012,inplace=True)
    fn['year'].replace(10,2010,inplace=True)
    fn['date']=''
    # Merging the year, month and date column to create a string for DateTime object.
    fn['date']= fn['year'].map(str)+fn['month'].map(str)+fn['day'].map(str)
    # Creating a DateTime object.
    fn['date_time']=''
    fn['date_time'] =  pd.to_datetime(fn['date'], format="%Y%m%d")
    # Sorting the file names according to the 
    # created DateTime object.
    fn.sort_values(['date_time'],inplace=True)
    # Created a list of sorted file names
    sorted_file_names = fn['file_name'].values
    return sorted_file_names

def reading_dataframes(file_names, Sheet_Name, path):
    """
    This function reads all the files in the sorted
    file names list as a dataframe
    
    Args(list): 
    file_names: Sorted file names list
    sheet_name: Sheet name in the excel file containing the data.
    
    Returns:
    Dictionary of dataframes in the order of the sorted file names.
    """
    # Empty dictionary to store all the dataframes according
    # to the order in the sorted files name list
    df = {}
    # Reading the dataframes
    for i in range(0,len(file_names)):
        df[i] = pd.read_excel(join(path,file_names[i]),sheet_name=Sheet_Name)
    return df

def concat_df(df_dict):
    """
    This function concatenates all the dataframes and edits
    the cycle index for the concatenated dataframes.
    
    Args:
    df_dict(dictionary): Dictionary of dataframes to be concatenated.
    
    Returns:
    A concatenated dataframe with editted cycle index
    
    """
    df_concat = None
    for k in range(0,len(df_dict)):
        if df_concat is None:
            df_next = df_dict[k]
            df_concat = pd.DataFrame(data=None, columns=df_next.columns)
            # df_next['Cycle'] = df_next['Cycle'] + max(df_pl12['Cycle'])
            df_concat = pd.concat([df_concat, df_next])
        else:
            df_next = df_dict[k]
            df_next['Cycle_Index'] = df_next['Cycle_Index'] + max(df_concat['Cycle_Index'])
            df_next['Test_Time(s)'] = df_next['Test_Time(s)'] + max(df_concat['Test_Time(s)'])
            df_next['Charge_Capacity(Ah)'] = df_next['Charge_Capacity(Ah)'] + max(df_concat['Charge_Capacity(Ah)'])
            df_next['Discharge_Capacity(Ah)'] = df_next['Discharge_Capacity(Ah)'] + max(df_concat['Discharge_Capacity(Ah)'])
            df_concat = pd.concat([df_concat, df_next])
    # Reset the index and drop the old index
    df_reset = df_concat.reset_index(drop=True)
    return df_reset

def capacity(df):
    """
    This function calculates the net capacity of the battery
    from the charge capacity and discharge capacity values.
    
    Args:
    df(dataframe): Concatenated dataframe which has the values of charge
    capacity and discharge capacity for which net capacity has to be
    calculated.
    
    Returns:
    Dataframe with net capacity of the battery for every point of the charge
    and discharge cycle.
    """
    # Grouping rows by the cycle index.
    group = df.groupby(['Cycle_Index']).count()
#     group['Cumu_count'] = pd.Series(np.random.randn(len(group)), index=group.index)
#     group['Cumu_count'] = group['Data_Point'].cumsum()
    
    # Get the indices when a cycle starts
    cycle_start_indices = group['Data_Point'].cumsum()
    
    # Get the charge_Ah per cycle
    # Create numpy array to store the old charge_Ah row, and then 
    # perform transformation on it, rather than in the pandas series 
    # this is a lot faster in this case
    charge_cycle_ah = np.array(df['Charge_Capacity(Ah)'])
    charge_ah = np.array(df['Charge_Capacity(Ah)'])
    
    for i in range(1, len(cycle_start_indices)):
        a = cycle_start_indices.iloc[i-1]
        b = cycle_start_indices.iloc[i]
        charge_cycle_ah[a:b] = charge_ah[a:b] - charge_ah[a-1]
    
    df['charge_cycle_ah'] = charge_cycle_ah
    
    # Get the discharge_Ah per cycle 
    discharge_cycle_ah = np.array(df['Discharge_Capacity(Ah)'])
    discharge_ah = np.array(df['Discharge_Capacity(Ah)'])
    
    for i in range(1, len(cycle_start_indices)):
        a = cycle_start_indices.iloc[i-1]
        b = cycle_start_indices.iloc[i]
        discharge_cycle_ah[a:b] =  discharge_ah[a:b] - discharge_ah[a-1]
        
    df['discharge_cycle_ah'] = discharge_cycle_ah 
    
    # This is the data column we can use for prediction. 
    # This is not totally accurate, as this still has some points that go negative, 
    # due to incorrect discharge_Ah values every few cycles. 
    # But the machine learning algorithm should consider these as outliers and 
    # hopefully get over it. We can come back and correct this. 
    df['capacity_ah'] = charge_ah - discharge_ah

    
    # Calculating charge and discharge for individual columns from cumulative data.
#     df['Charge'] = pd.Series(np.random.randn(len(df)), index=df.index)
#     df['discharge'] = pd.Series(np.random.randn(len(df)), index=df.index)
#     cycle = []
#     cycle = group['Cumu_count']
#     df['Charge'][0:cycle[1]] = df['Charge_Capacity(Ah)'][0:cycle[1]]
#     df['discharge'][0:cycle[1]] = df['Discharge_Capacity(Ah)'][0:cycle[1]]
#     # Calculating net capacity using the calculated charge and discharge values.
#     for i in range(1,len(cycle)):
#         df['Charge'][cycle[i]:cycle[i+1]] = df['Charge_Capacity(Ah)'][cycle[i]:cycle[i+1]]-df['Charge_Capacity(Ah)'][cycle[i]]
#         df['discharge'][cycle[i]:cycle[i+1]] = df['Discharge_Capacity(Ah)'][cycle[i]:cycle[i+1]]-df['Discharge_Capacity(Ah)'][cycle[i]]
#     df['Capacity'] = pd.Series(np.random.randn(len(df)), index=df.index)
#     df['Capacity'] = df['Charge'] - df['discharge']
    return df
