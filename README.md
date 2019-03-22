[![Build Status](https://travis-ci.com/chintanp/BattDeg.svg?branch=master)](https://travis-ci.com/chintanp/BattDeg) [![Coverage Status](https://coveralls.io/repos/github/chintanp/BattDeg/badge.svg?branch=master)](https://coveralls.io/github/chintanp/BattDeg?branch=master) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Documentation Status](https://readthedocs.org/projects/battdeg/badge/?version=latest)](https://battdeg.readthedocs.io/en/latest/?badge=latest)

# BattDeg


## Introduction

Lithium-ion batteries degrade during in any application, be it a cell-phone or a laptop, or an electric vehicle. 
While the exact cause of degradation is not fully understood, it is known to be affected by the operating conditions like 
charge/discharge current, temperature etc. With `battdeg` we are trying to predict the degradation in a battery given a few cycles of operation. 
We use a seq2seq LSTM model in Keras to do the prediction and the model has been trained on the CALCE data. The users can also train the models using their own dataset for their batteries
and operating conditions. 

## Installation 

To install, use `pip install battdeg`, and then you can import the module `battdeg` in your python script or jupyter notebook.

## Usage 

The module is still under development and API may change over time. Currently: 
1. Get the CALCE data and unzip it. 
2. Read in the CALCE data. The cycling data available from CALCE is separated into files. The file_reader() functions provide the capability of reading the files and creating a dataframe from data from all files. 
3. 


## For development

1. Install python version 3.6. 
2. Install the dependencies from requirements.txt using `pip3 install -r requirements.txt`
3. Run `npm install` to install grunt. 
4. In the root folder in terminal, run `grunt`. This will automatically run the unit tests in battdeg folder when you save any Python file in the battdeg folder. This includes your unit tests and modules. 
5. Remember to TDD. 

## Future Scope 

