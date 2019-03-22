[![Build Status](https://travis-ci.com/chintanp/BattDeg.svg?branch=master)](https://travis-ci.com/chintanp/BattDeg) [![Coverage Status](https://coveralls.io/repos/github/chintanp/BattDeg/badge.svg?branch=master)](https://coveralls.io/github/chintanp/BattDeg?branch=master) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Documentation Status](https://readthedocs.org/projects/battdeg/badge/?version=latest)](https://battdeg.readthedocs.io/en/latest/?badge=latest)

# BattDeg

## Usecases for the project

* To predict the degradation in a lithium-ion battery using the few cycles of usage. 

## Components

## Usage Instructions 

The functions are written according to the datafiles available for PL samples, CX2 and CS2 cells available on the Center for  Advanced Life Cycle Engineering(CALCE) Battery Research Group [website](https://web.calce.umd.edu/batteries/data.htm)

This Python package contains following functions: 

1. `file_reader()`: This function can be used to format the input dataframe such that it can be used by the 'model_prediction' function. 
2. `model_prediction()`: This function takes the formatted dataframe and predicts the discharge capacity values.

For a new dataset, below are the usage instructions:  
* Input data format   
In the input dataframe, the essential columns must be named as below:

| Data                   | Column Name  |
|------------------------|--------------|
| Current                | Current(A)   |
| Voltage                | Voltage(V)   |
| Discharge capacity(Ah) | Discharge_Ah |
| Charge capacity(Ah)    | Charge_Ah    |

* If the data is cumulative, the above mentioned two functions can be used.

* If the data is not cumulative, the dataframe can be formatted as required for use by 'model_prediction' by using the following function:  

1.`data_formatting()` : This function drops all the unnecessary columns in the input dataframe and prepares the dataframe for use by 'model_prediction' function.


## For development

1. Install python version 3.6. 
2. Install the dependencies from requirements.txt using `pip3 install -r requirements.txt`
3. Run `npm install` to install grunt. 
4. In the root folder in terminal, run `grunt`. This will automatically run the unit tests in battdeg folder when you save any Python file in the battdeg folder. This includes your unit tests and modules. 
5. Remember to TDD. 

## Future Scope 

1. Convert the files from .mat format to .csv in Python. 
2. Include ability to train for multiple chemistries, voltage windows etc. 
3. Deploy the solution as a web-service and create a web-UI. 

