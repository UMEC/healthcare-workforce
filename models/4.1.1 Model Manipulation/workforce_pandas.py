
# coding: utf-8

# # Analytical Model Pandas Class

# In[9]:


# coding: utf-8


# This module extracts all the csv files found in a specified directory and loads them into a dictionary of pandas dataframes
# 
# Each dataframe is truncated at the *end* position as specified in the first column of each imported CSV file.
# 
# The provided functions allow the list of dataframes to be retrieved and access to the dataframes themselves
# 
# Designed to be maintained in Jupyter Notebook to assist learning, it is converted to standard Python via : 
# 
# ### jupyter nbconvert --to script workforce_pandas.ipynb
# 

# In[10]:


import pandas as pd
import json
import sys
import os
import re


# This function determines if the script is running server side or in a Jupyter notebook (where the __file__ variable is not accessible)

# In[11]:


def type_of_script():
    ''' Returns jupyter if running in a notebook, otherwise returns server
    '''
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'jupyter'
    except:
        return 'server'


# The choice of directory path is determined by the run-time environment

# In[12]:


if type_of_script()=='jupyter':
    directory = "../data/data_input_component_csv/"
else:
    directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../data/data_input_component_csv/")


# The dataframes dictionary is used to create a indexed home for all the pandas data frames.  Their CSV file names, which were automatically generated from their sheet names by the Excel import service will then used as their panda names.

# The sheets array will be used to store a full list of the names of all the panda dataframes created

# This section has two main functions.  First, it will scan the prescribed directory for all the files with .csv as their suffix.  For each file found, a loop begins.  
# 
# The name of the csv file (minus the suffix) is asigned to the sheet variable.  This is appended to the sheets array.  
# 
# The csv file is then read into a pandas dataframe.  This dataframe is stored in the frames dictionary under the name of the sheet.  The dataframe is then scanned looking for the value <<end>> in the first column.  This is deemed to be the end of the dataframe and the dataframe is truncated to the row above this.
#     
# The loop continues until all the .csv files have been read and processed.
# 
# Trimming the length first (according to an easy to use human clip point) then makes trimming the columns much more reliable...

# In[13]:


dataframes = {}
sheets = []
for f in os.listdir(directory):
    if f.endswith(".csv"):
        sheet = os.path.splitext(f)[0]
        sheets.append(sheet)
        dataframes[sheet] = pd.read_csv(directory + "/" + f)
        for j in range(len(dataframes[sheet])):
            if dataframes[sheet].iloc[j,0] =="<<end>>":
                break
        dataframes[sheet] = dataframes[sheet].head(j)
        dataframes[sheet]=dataframes[sheet].dropna(axis=1,how='all')


# In[14]:


def get_dataframe_list():
    '''
    Returns an array containing the list of all the panda dataframes that
    have been loaded
    '''
    return sheets
def get_dataframe_dict():
    '''
    Returns the dictionary of all the pandas dataframes
    '''
    return dataframes
def get_dataframe(name):
    '''
    Returns a dataframe based on the name provided, if no dataframe of 
    that name is present then a string will be returned

        Parameters
        ----------
            name : str, mandatory
                The name of the dataframe requested
    '''
    try:
        return dataframes[name]
    except:
        return "No dataframe of that name"

