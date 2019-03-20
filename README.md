[![Build Status](https://travis-ci.com/chintanp/BattDeg.svg?branch=master)](https://travis-ci.com/chintanp/BattDeg) [![Coverage Status](https://coveralls.io/repos/github/chintanp/BattDeg/badge.svg?branch=master)](https://coveralls.io/github/chintanp/BattDeg?branch=master) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Documentation Status](https://readthedocs.org/projects/battdeg/badge/?version=latest)](https://battdeg.readthedocs.io/en/latest/?badge=latest)

# BattDeg

## Usecases for the project

* To predict the degradation in a lithium-ion battery using the few cycles of usage. 

## Components

## Usage Instructions 

This Python package contains following functions: 

1. `PL_samples_file_reader()`: This function reads the files from PL_samples experiment. TODO: Test for other files this PL12 14 folder, then other folders in PL_samples experiment. Then work on optimization. 


## For development

1. Install python version 3.6. 
2. Install the dependencies from requirements.txt using `pip3 install -r requirements.txt`
3. Run `npm install` to install grunt. 
4. In the root folder in terminal, run `grunt`. This will automatically run the unit tests in battdeg folder when you save any Python file in the battdeg folder. This includes your unit tests and modules. 
5. Remember to TDD. 

## Future Scope 

1. Convert the files from .mat format to .csv in Python. 
2. Include ability to train for multiple chemistries, voltage windows etc. 
3. 
