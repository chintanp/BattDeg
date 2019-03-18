import pandas as pd
import numpy as np
import datetime
import os, sys
import re
import xlrd
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import seaborn as sns
import pytest # automatic test finder and test runner
    
import hypothesis.strategies as st
from hypothesis import assume, given, settings, Verbosity
from hypothesis.strategies import integers as ints
from hypothesis.extra.pandas import column, data_frames, indexes, range_indexes, columns

# To import files from the parent directory 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cx2reader as cx
from cx2reader import CX2_sample_file_reader
from cx2reader import file_name_sorting
from cx2reader import reading_dataframes
from cx2reader import concat_df
from cx2reader import capacity

# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Path for data for testing
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = join(base_dir, 'data')
# data_path_cx2_16 = data_path

###########################################################################
####################### Tests for `CX2_sample_file_reader` ################
###########################################################################

# This test will test the function `CX2_sample_file_reader` for bad input
def test_CX2_sample_file_reader():

	#Inputs with wrong type for data_dir
	dd1 = 12
	fnf1 = 'data'
	sn1 = 'Channel_1-006'

	#Input with wrong type of sheet name
	dd1 = base_dir
	fnf2 = 'data'
	sn2 = 123

	#Input with wrong type of file name format
	dd3 = base_dir
	fnf2 = 'abc'
	sn3 = 'Channel_1-006'

	#Input with wrong file not found error
	dd4 = data_path
	fnf4 = "abc"
	sn4 = 'Channel_1-006'

	#The wrong type input should raise a TypeError
	with pytest.raises(TypeError):
		CX2_sample_file_reader(dd1, fnf1, sn1)

	with pytest.raises(TypeError):
		CX2_sample_file_reader(dd2, fnf2, sn2)

	with pytest.raises(TypeError):
		CX2_sample_file_reader(dd3, fnf3, sn3)

	with pytest.raises(FileNotFoundError):
		CX2_sample_file_reader(dd5, fnf5, sn4)

	return

# Test the output type of the function
def test_CX2_sample_file_reader():

	#Correct inputs
	dd = base_dir
	fnf = 'data'
	sn = 'Channel_1-006'

	# Run the function with these inputs
	result = CX2_sample_file_reader(dd, fnf, sn)
	assert isinstance(result,pd.DataFrame), 'Output is not a dataframe'

# Test the output of the function 'file_name_sorting'
files = listdir(data_path)
file_name_list = list(filter(lambda x: x[-5:]=='.xlsx' , files))
def test_file_name_sorting():
	sorted_list = file_name_sorting(file_name_list)
	assert isinstance(sorted_list,np.ndarray),'Output is not a list'

# Test the output of the function 'reading_dataframes'
file_names = file_name_sorting(file_name_list)
Sheet_Name = 1
path = data_path
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
