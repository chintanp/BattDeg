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
from battdeg import cx2_file_reader
from battdeg import file_name_sorting
from battdeg import reading_dataframes
from battdeg import concat_df
from battdeg import capacity
from battdeg import data_formatting
from battdeg import series_to_supervised
from battdeg import long_short_term_memory
from battdeg import model_training
from battdeg import model_prediction
from battdeg import file_reader

# Path for data for testing
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = join(module_dir,'models')
data_path = join(module_dir, 'data')
data_path_pl12_14 = join(data_path,'PL12')

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

###########################################################################
####################### Tests for `cx2_file_reader` ###########################
###########################################################################

# This test will test the function `cx2_file_reader` for bad input
def test_cx2_file_reader():

	#Inputs with wrong type for data_dir
	dd1 = 12
	fnf1 = 'CX2_16'
	sn1 = 1

	#Input with wrong type of sheet name
	dd2 = data_path
	fnf2 = 'CX2_16'
	sn2 = 123.5

	#Input with wrong type of file name format
	dd3 = data_path
	fnf2 = 'abc'
	sn3 = 1

	#Input with wrong file not found error
	dd4 = data_path
	fnf4 = "abc"
	sn4 = 1

	#The wrong type input should raise a TypeError
	with pytest.raises(TypeError):
		cx2_file_reader(dd1, fnf1, sn1)

	with pytest.raises(TypeError):
		cx2_file_reader(dd2, fnf2, sn2)

	with pytest.raises(TypeError):
		cx2_file_reader(dd3, fnf3, sn3)

	with pytest.raises(FileNotFoundError):
		cx2_file_reader(dd5, fnf5, sn4)

	return

# Test the output type of the function
#Correct inputs
dd = data_path
fnf = 'CX2_16'
data_path_cx2_16 = join(data_path,'CX2_16')
sn = 1
# Run the function with these inputs
result = cx2_file_reader(dd, fnf, sn)
def test_cx2_file_reader():
	assert isinstance(result,pd.DataFrame), 'Output is not a dataframe'

# Test the output of the function 'file_name_sorting'
files = listdir(data_path_cx2_16)
file_name_list = list(filter(lambda x: x[-5:]=='.xlsx' , files))
def test_file_name_sorting():
	sorted_list = file_name_sorting(file_name_list)
	assert isinstance(sorted_list,np.ndarray),'Output is not a list'

# Test the output of the function 'reading_dataframes'
file_names = file_name_sorting(file_name_list)
Sheet_Name = 1
path = join(data_path,'CX2_16')
df = reading_dataframes(file_names, Sheet_Name, path)
def test_reading_dataframes():
	assert isinstance(df, dict), 'Output is not a dictionary of dataframes'

# Test the output of the function 'concat_df'
merged_df = concat_df(df)
def test_concat_df():
	assert isinstance(merged_df, pd.DataFrame),'Output is not a dataframe'
	
# Test the output of the function 'capacity'
capacity_df = capacity(merged_df)
def test_capacity():
	assert isinstance(capacity_df,pd.DataFrame),'Output is not a dataframe'

# Test the output of the function 'data_formatting'
formatted_df = data_formatting(capacity_df)
def test_data_formatting():
	assert isinstance(formatted_df,pd.DataFrame),'Output is not a dataframe'
	assert len(formatted_df.columns) == 3,'The number of columns in the output is not 3 as expected'

# Test the output of the function 'series_to_supervised'
training_data = series_to_supervised(formatted_df)
def test_series_to_supervised():
	assert isinstance(training_data, pd.DataFrame),'Output is not a dataframe'
	assert len(training_data.columns) == 4,'The number of columns in the output is not 4 as expected'

# Test the output of the function 'long_short_term_memory'
model_loss, yhat = long_short_term_memory(training_data)
def test_long_short_term_memory():
	assert isinstance(yhat, np.ndarray),'Response of the test dataset is not an array'
	assert isinstance(model_loss, dict),'Loss function is not a dictionary'
	assert yhat.shape[1] == 1,'The number of columns in the output is not 1 as expected'

# Test the output of the function 'model_training'
model_loss, yhat = model_training(dd, fnf, sn)
def test_model_training():
	assert isinstance(yhat, np.ndarray),'Response of the test dataset is not an array'
	assert isinstance(model_loss, dict),'Loss function is not a dictionary'
	assert yhat.shape[1] == 1,'The number of columns in the output is not 1 as expected'

# # Test the output of the function 'model_predict'
y_predicted = model_prediction(formatted_df)
def test_model_prediction():
	assert isinstance(y_predicted, np.ndarray),'Response of the test dataset is not an array'
	assert y_predicted.shape[1] == 1,'The number of columns in the output is not 1 as expected'

# Test the output of the function 'file_reader'
file_indices1 = [1, 2, 3]
sheet_name = 1
data_dir = data_path
file_name_format = 'CX2_16'
df_output = file_reader(data_dir, file_name_format, sheet_name, file_indices1)
def test_file_reader():
   assert isinstance(df_output,pd.DataFrame), 'Output is not a dataframe'
   assert len(df_output.columns) == 3,'The number of columns in the output is not 3 as expected'
