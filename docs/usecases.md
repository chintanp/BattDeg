# Usecases for the project BattDeg

 We aim for the package BattDeg to serve these two usecases: 
 
 1. Generate dataframes from CALCE data files. 
    
    The CALCE data is divided into files and this makes it rather cumbersome for use. Since this is so interesting, and open, we wrote functions 
    to read in the following datasets: CS2, CX2 and PL Samples. For the said datasets, we also create columns to calculate the per cycle charge and 
    discharge capacities and calculate the total capacity in the cycle by subtracting the two. You can use the functions as described in teh documentation and examples to generate the dataframes for your use.


2. To predict the degradation in a lithium-ion battery using the few cycles of usage. 
    
    Once the data from files is converted into a usable format, we want to use it for prediction of battery capacity. The seq2seq encoder decoder LSTM model in Keras is used for this forecasting. The code is based on several articles on Machine Learning Mastery, 
    like [this](https://machinelearningmastery.com/how-to-develop-lstm-models-for-multi-step-time-series-forecasting-of-household-power-consumption/).


