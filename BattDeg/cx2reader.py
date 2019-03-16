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

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


# Wrapping function to calculate LSTM model_loss, response to testing data set
# and response to new training data set.

def capacity_fade(data_dir, file_name_format, Sheet_Name, prediction_data):
    """
    This function predicts the discharge capacity of a battery given the time
    series data of the first few charging-discharging cycles of the battery.
    This function also converts the new time series dataset into a supervised 
    learning dataset.
    
    Args:
        data_dir (string): This is the absolute path to the data directory. 
        file_name_format (string): Format of the filename, used to deduce other files.
        Sheet_Name(string or int): Sheet name or sheet number in the excel file containing
        the relevant data.

    Returns:
        model_loss(dictionary): Returns the history dictionary (more info to be added)
        y_hat(array): Predicted response for the testing dataset.
        y_prediction(array): Predicted response for the completely new dataset
        (The input has to be the time series cycling data including values of 
         Current, Voltage and Discharge Capacity)
    """
    # The function 'CX2_sample_file_reader' is used to read all the excel files
    # in the given path and convert the given cumulative data into individual cycle data.
    individual_cycle_data = CX2_sample_file_reader(data_dir, file_name_format, Sheet_Name)

    # The function 'data_formatting' is used to drop the unnecesary columns 
    # from the training data i.e. only the features considered in the model
    # (Current, Voltage and Discharge capacity) are retained.
    formatted_data = data_formatting(individual_cycle_data)

    # The function 'series_to_supervised' is used to frame the time series training
    # data as supervised learning dataset.
    learning_df = series_to_supervised(formatted_data, n_in=1, n_out=1, dropnan=True)

    # The function 'long_short_term_memory' is used to train the model
    # and predict response for the new input dataset.
    model_loss, y_hat, y_prediction = long_short_term_memory(learning_df,prediction_data)

    return model_loss, y_hat, y_prediction


# Wrapping function only to merge and convert cumulative data to
# individual cycle data.
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

    if not isinstance(Sheet_Name,str or int):
        raise TypeError('Sheet_Name format is not of type string or integer')
        
    if not os.path.exists(join(data_dir,file_name_format)):
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
    fn['date']=''
    # Merging the year, month and date column to create a string for DateTime object.
    fn['date']= fn['year'].map(str)+fn['month'].map(str)+fn['day'].map(str)
    # Creating a DateTime object.
    fn['date_time']=''
    fn['date_time'] =  pd.to_datetime(fn['date'], format="%y%m%d")
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
            df_next['Cycle_Index'] = np.array(df_next['Cycle_Index'])+ max(np.array(df_concat['Cycle_Index']))
            df_next['Test_Time(s)'] = np.array(df_next['Test_Time(s)']) + max(np.array(df_concat['Test_Time(s)']))
            df_next['Charge_Capacity(Ah)'] = np.array(df_next['Charge_Capacity(Ah)']) + max(np.array(df_concat['Charge_Capacity(Ah)']))
            df_next['Discharge_Capacity(Ah)'] = np.array(df_next['Discharge_Capacity(Ah)']) + max(np.array(df_concat['Discharge_Capacity(Ah)']))
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
    df['capacity_ah'] = df['charge_cycle_ah'] - df['discharge_cycle_ah']

    return df


def data_formatting(merged_df):
    """
    This function formats the merged dataframe so that it can be used to frame the given
    time series data as a supervised learning dataset.
    
    Args:
        merged_df(dataframe): The merged dataframe which can be obtained by using the
        function 'CX2_sample_file_reader'
    
    Returns:
        A numpy array with only values required to frame a time series as a
        supervised learning dataset.
    """
    column_names = ['Current(A)','Voltage(V)','discharge_cycle_ah']
    merged_df = merged_df[column_names]
    formatted_df = merged_df.astype('float32')
    return formatted_df


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """
    Frame a time series as a supervised learning dataset.
    Arguments:
        data: Sequence of observations as a list or NumPy array.
        n_in: Number of lag observations as input (X).
        n_out: Number of observations as output (y).
        dropnan: Boolean whether or not to drop rows with NaN values.
    Returns:
        Pandas DataFrame of series framed for supervised learning.
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    sl_df = pd.concat(cols, axis=1)
    sl_df.columns = names
    # drop rows with NaN values
    if dropnan:
        sl_df.dropna(inplace=True)
    sl_df.drop(sl_df.columns[[3,4]],axis=1,inplace=True)
    return sl_df


def long_short_term_memory(model_data,prediction_data):
    """
    This function splits the input dataset into training
    and testing datasets. The keras LSTM model is then 
    trained and tested using the respective datasets.

    Args:
        model_data(dataframe): Values of input and output variables
        of time series data framed as a supervised learning dataset.
        prediction_data(dataframe): Values of input variables of time series
        data framed as a supervised learning dataset.

    Returns:
        model_loss(dictionary): Returns the history dictionary (more info to be added)
        y_hat(array): Predicted response for the testing dataset.
        y_prediction(array): Predicted response for the completely new dataset. 
    """
    # Splitting the input dataset into training and testing data
    train,test = train_test_split(model_data, test_size=0.2, random_state=944)
    # split into input and outputs
    train_X, train_y = train[train.columns[0:3]].values, train[train.columns[3]].values
    test_X, test_y = test[test.columns[0:3]].values, test[test.columns[3]].values
    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

    # Designing the network
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    # Fitting the network with training and testing data
    history = model.fit(train_X, train_y,epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=0, shuffle=False)
    model_loss = history.history
    # Prediction for the test dataset.
    yhat = model.predict(test_X)
    # Predicting response for a different dataset.
    # Converting the time series data into supervised learning dataset for the LSTM model.
    pred_data = series_to_supervised(prediction_data, n_in=1, n_out=1, dropnan=True) 
    prediction_data = pred_data[pred_data.columns[0:3]].values
    # Reshaping the input dataset.
    prediction_data = prediction_data.reshape((prediction_data.shape[0],1,prediction_data.shape[1]))
    y_prediction = model.predict(prediction_data)
    return model_loss, yhat, y_prediction
