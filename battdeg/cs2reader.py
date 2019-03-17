"""
This module can be used to read cycling data of the CS2 type cells as
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

def CS2_sample_file_reader(data_dir, file_name_format, Sheet_Name):
    """
    This function reads in the data for CS2 samples experiment and returns
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
    # Get the capacity of each cycle and combine together
    # using the 'concat_df' function.
    capacity_data = concat_df(sorted_df)
    
    # Returns the dataframe with new cycle indices and capacity data.
    return capacity_data

def file_name_sorting(file_names):
    """
    This function sorts all the file names according to the date
    on the file name.
    
    Args:
    file_name(list): List containing all the file names to be read
    
    Returns:
    A list of file names sorted according to the date on the file name.
    
    """
    fn = pd.DataFrame(data = file_names,columns = ['file_name'])
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
    fn['year'].replace(13,2013,inplace=True)
    fn['year'].replace(14,2014,inplace=True)
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
    sorted_file_names = fn['file_name'].values.tolist()
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
    i=0
    df = {}
    for filename in file_names:
        df[i] = pd.read_excel(join(path,file_names[i]), sheet_name=Sheet_Name)
        i = i+1
    return df

def concat_df(df_dict):
    """
    This function edits the cycle index for the each dataframes.
    
    
    Args:
    df_dict(dictionary): Dictionary of dataframes to be concatenated.
    
    Returns:
    A concatenated dataframe with editted cycle index
    
    """
    # Empty dataframe to store all the dataframes according
    combined_dataframe=None
    # Use loop to load other dataframes
    for j in range(len(df_dict)):
        dataframe=df_dict[j]
        # make an index
        dataframe['Index']=pd.Series(np.linspace(1,len(dataframe),len(dataframe)),index=dataframe.index)
        # make an empty group to grupby the cycle index
        group=pd.DataFrame()
        group = dataframe.groupby(['Cycle_Index']).count()
        # Get the indices when a cycle starts
        cycle_start_indices = group['Index'].cumsum()

        # Get the charge_Ah per cycle
        # Create numpy array to store the old charge_Ah row, and then 
        # perform transformation on it, rather than in the pandas series 
        # this is a lot faster in this case
        charge_cycle_ah = np.array(dataframe['Charge_Capacity(Ah)'])
        charge_ah = np.array(dataframe['Charge_Capacity(Ah)'])

        for i in range(1, len(cycle_start_indices)):
            a = cycle_start_indices.iloc[i-1]
            b = cycle_start_indices.iloc[i]
            charge_cycle_ah[a:b] = charge_ah[a:b] - charge_ah[a-1]

        dataframe['charge_cycle_ah'] = charge_cycle_ah

        # Get the discharge_Ah per cycle 
        discharge_cycle_ah = np.array(dataframe['Discharge_Capacity(Ah)'])
        discharge_ah = np.array(dataframe['Discharge_Capacity(Ah)'])

        for i in range(1, len(cycle_start_indices)):
            a = cycle_start_indices.iloc[i-1]
            b = cycle_start_indices.iloc[i]
            discharge_cycle_ah[a:b] =  discharge_ah[a:b] - discharge_ah[a-1]

        dataframe['discharge_cycle_ah'] = discharge_cycle_ah
        if combined_dataframe is None:
            dataframe['Cycle_Index']=dataframe['Cycle_Index']+0
            combined_dataframe=dataframe
        else:
            dataframe['Cycle_Index']=dataframe['Cycle_Index']+max(combined_dataframe['Cycle_Index'])
            combined_dataframe=combined_dataframe.append(dataframe)
    # get the data of capacity
    combined_dataframe['Capacity']=combined_dataframe['charge_cycle_ah']-combined_dataframe['discharge_cycle_ah']
    df_reset = combined_dataframe.reset_index(drop=True)
    return df_reset
