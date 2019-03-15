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
from battdeg import PL_samples_file_joiner


# Path for data for testing
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = join(base_dir, 'data')
data_path_pl12_14 = join(data_path, 'PL 12,14')

###########################################################################
####################### Tests for `PL_samples_file_joiner` ################
###########################################################################

# This test will test the function `PL_samples_file_joiner` for bad input
def test_PL_samples_file_joiner_BadIn():
    
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
       PL_samples_file_joiner(dd1, fnf1, file_indices1)
    
    with pytest.raises(TypeError):
       PL_samples_file_joiner(dd2, fnf2, file_indices2)
       
    with pytest.raises(TypeError):
       PL_samples_file_joiner(dd3, fnf3, file_indices3)
    
    with pytest.raises(TypeError):
       PL_samples_file_joiner(dd4, fnf4, file_indices4)
    
    with pytest.raises(FileNotFoundError):
       PL_samples_file_joiner(dd5, fnf5, file_indices5)
     
    ### TODO: Add tests for checking the validity of the path
    
    return


# Test the output type of the function 
def test_PL_samples_file_joiner_Type():
    
    # Correct inputs
    dd1 = data_path_pl12_14
    fnf1 = "PL12(4).csv"
    file_indices1 = [1, 2, 3]
    
    # Run the function with these inputs 
    result = PL_samples_file_joiner(dd1, fnf1, file_indices1)
    
    # Check if the output is of type pd.DataFrame
    assert isinstance(result, pd.DataFrame), "The type of the return value is not of type Pandas.DataFrame"
    
    return 
