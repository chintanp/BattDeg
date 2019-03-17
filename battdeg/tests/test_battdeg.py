import pandas as pd
import numpy as np
import datetime
import os, sys
import re
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import seaborn as sns
import pytest # automatic test finder and test runner

# To import files from the parent directory 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import battdeg as bd
from battdeg import pl_samples_file_reader
from battdeg import date_time_converter
from battdeg import get_dict_files
from battdeg import concat_dict_dataframes
from battdeg import get_cycle_capacities

# Path for data for testing
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = join(module_dir, 'data')
data_path_pl12_14 = data_path

###########################################################################
####################### Tests for `pl_samples_file_reader` ################
###########################################################################

# This test will test the function `pl_samples_file_reader` for bad input
def test_pl_samples_file_reader_BadIn():
    
    # Inputs with wrong type for data_dir
    dd1 = 123
    fnf1 = "PL12(4).csv"
    file_indices1 = [1, 2, 3]
    
    # Inputs with wrong type for input_file_indices
    dd2 = data_path_pl12_14
    fnf2 = "PL12(4).csv"
    file_indices2 = 1
    
    dd3 = data_path_pl12_14
    fnf3 = "PL12(4).csv"
    file_indices3 = ['a', 'b', 'c']
    
    # Inputs with wrong type for file_name_format
    dd4 = data_path_pl12_14
    fnf4 = 123
    file_indices4 = [1, 2, 3]
    
    # Inputs with wrong file not found error
    dd5 = data_path_pl12_14
    fnf5 = "123"
    file_indices5 = [1, 2, 3]
    
    # The wrong type input should raise a TypeError
    with pytest.raises(TypeError):
       pl_samples_file_reader(dd1, fnf1, file_indices1)
    
    with pytest.raises(TypeError):
       pl_samples_file_reader(dd2, fnf2, file_indices2)
       
    with pytest.raises(TypeError):
       pl_samples_file_reader(dd3, fnf3, file_indices3)
    
    with pytest.raises(TypeError):
       pl_samples_file_reader(dd4, fnf4, file_indices4)
    
    with pytest.raises(FileNotFoundError):
       pl_samples_file_reader(dd5, fnf5, file_indices5)
     
    ### TODO: Add tests for checking the validity of the path
    
    return


# Test the output type of the function 
def test_pl_samples_file_reader_Type():
    
    # Correct inputs
    dd1 = data_path_pl12_14
    fnf1 = "PL12(4).csv"
    file_indices1 = [1, 2, 3]
    
    # Run the function with these inputs 
    result = pl_samples_file_reader(dd1, fnf1, file_indices1)
    
    # Check if the output is of type pd.DataFrame
    assert isinstance(result, pd.DataFrame), "The type of the return value is not of type Pandas.DataFrame"
    
    return 


###########################################################################
####################### Tests for `date_time_converter()` ################
###########################################################################

# Test the date time converter function
def test_date_time_converter_BadIn():
    
    dt_in = 123
    
    with pytest.raises(TypeError):
       date_time_converter(dt_in)
        
    return


###########################################################################
####################### Tests for `get_dict_files()` ################
###########################################################################

def test_get_dict_files_Type():
    
    # Correct inputs
    dd1 = data_path_pl12_14
    fnf1 = "PL12(4).csv"
    file_indices1 = [1, 2, 3]
    
    result = get_dict_files(dd1, fnf1, file_indices1)
    
    assert isinstance(result, dict), "The type of output from the function get_dict_files should be a dictionary"
    
    return

###########################################################################
####################### Tests for `concat_dict_dataframes()` ################
###########################################################################

def test_concat_dict_dataframes_BadIn():
    
    # Input not of the right type
    dict_ordered1 = 123
    
    # Input not of the right type
    dict_ordered2 = {'a': pd.DataFrame()}
    
    # Input not of the right type
    dict_ordered3 = {1: [1, 2, 3]}

    # test that the dataframe has the named columns that we expect 
    dict_ordered4 = {1: pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})}
    
    with pytest.raises(TypeError):
       concat_dict_dataframes(dict_ordered1)
       
    with pytest.raises(TypeError):
       concat_dict_dataframes(dict_ordered2)
       
    with pytest.raises(TypeError):
       concat_dict_dataframes(dict_ordered3)

    
    with pytest.raises(Exception, match = "the dataframe doesnt have the columns 'Cycle'" +
                            ", 'Charge_Ah', 'Discharge_Ah', " + 
                            "'Time_sec', 'Voltage_Volt', 'Current_Amp' "):
        concat_dict_dataframes(dict_ordered4)
    
    return 


# test whether the output type is a dataframe
def test_concat_dict_dataframes_Type():
    
    # Good input 
    # dict_ordered1 = {1 :  
    # result = 
    return 


###########################################################################
####################### Tests for `get_cycle_capacities()` ################
###########################################################################


def test_get_cycle_capacities_Type():
    
    
    return


def test_get_cycle_capacities_Type():
    
    df_out1 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    
    with pytest.raises(Exception, match = "the dataframe doesnt have the columns 'Cycle'" +
                            ", 'Charge_Ah', 'Discharge_Ah', " + 
                            "'Time_sec', 'Voltage_Volt', 'Current_Amp' "):
        get_cycle_capacities(df_out1)
    
    return
