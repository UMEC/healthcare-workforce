
# coding: utf-8

# # Workforce Model

# This program creates a pandas from the imported Excel spreadsheet.
# 
# It can return three types of information as a result of requests from the front end:
# 
# * {"request_type": "available_years"}
# * {"request_type": "geo_profile"}
# * {"request_type": "provider_profile"}
# * {"request_type": "save_model"}
# * {"request_type": "load_model", "value": "sample_model_id", "directory" : "/sample/directory"}
# 
# It can also process deltas to this information as a result of user input from the front end:
# 
# * {JSON_string}
# 
# The JSON_string will be formatted similarly to the request types.
# 
# In response to these deltas, it will run the relevant optimization model depending upon the
# deltas and constraints provided in the JSON string.
# 
# ### jupyter nbconvert --to script workforce_model.ipynb
# 

# The model uses the imported Excel sheets that are created by the workforce_pandas module

# In[1]:


import workforce_pandas as wfpd
import json
import sys
import pickle
import base64
command="null"
provider_type="null"


# In[2]:


wfpd.sheets


# The model takes the input of a JSON string from stdin

# In[3]:


value = "null"
command_string = input("")


# All responses are formatted and sent using the respond function below:

# In[4]:


def respond(response_msg,verb,object,error_msg=None):
    """Prints a JSON formatted service response to std out and exits the program

        Parameters
        ----------
        response_msg : str, mandatory
            The message included in the response attribute of the JSON out
        verb : str, mandatory
            The command that was received (if any)
        object: str, mandatory
            The target for the command that was received (if any)
        error_msg : str, optional
            An error message string
    """
    if (error_msg != None):
        response_msg = '{"error_msg":"' + error_msg + '"}'
    response = '{"request":' + command_string + ',"response":' + response_msg + '}'
    print (response)
    sys.exit(0)


# This input command is parsed into one to three strings, or an exception is raised and then passed back to the caller

# In[5]:


# parse the command line argument into a JSON object
try:
    parsed_command = json.loads(command_string)
except Exception as e:
    respond(None,command,provider_type, "ERROR: Invalid argument - not in JSON format: "+str(e))
if "request_type" in parsed_command:
    command = str(parsed_command["request_type"])
else:
    respond(None,command,provider_type, "ERROR: Invalid argument - no request_type defined")
if "value" in parsed_command:
    value = str(parsed_command["value"])
if "directory" in parsed_command:
    directory = str(parsed_command["directory"])


# The next two functions are used to manipulate the automatically generated JSON strings as they often don't conform to the format that we require in our responses

# In[6]:


def strip_brackets(JSON_string):
    """Strips the square brackets from a JSON string

        Parameters
        ----------
        JSON_string : str, mandatory
            The JSON string to strip the leading and trailing end square brackets from
    """
    result = JSON_string.strip("[]")
    return result


# In[7]:


def strip_curlies(JSON_string):
    """Strips the curly brackets from a JSON string

        Parameters
        ----------
        JSON_string : str, mandatory
            The JSON string to strip the leading and trailing curly brackets from
    """
    result = JSON_string.strip("{}")
    return result


# The next three functions manipulate pandas dataframes in various ways to assist in turning them into JSON strings.  _df_to_json_attri is useful for single simple rows and uses the in-built functions to perform the transform.  The _sub_json_object_ and _frame_sub_json_object_ manipulate the dataframes themselves to categories of related data in dataframes for conversion into JSON strings

# In[8]:


def sub_json_object(source,index_column,value):
    """Takes a wfpd dataframe (i.e. a csv sheet in pandas form)
        and filters it on provided value on its index_column.  The
        index column is then removed, effectively providing a table
        of related data.  This table is then returned as a dataframe.
        Useful function for transforming pandas JSON friendly structures.
    
        Works well for simple rows, but is a little naive in terms of transformation for
        multiple row tables or those with categories.

        Parameters
        ----------
        source : string
            The name of the wfpd dataframe (aka Excel sheet name)
        index_column : string
            The name of the column on the wfpd dataframe to filter on
        value : string
            The value to filter on
    """
    dataframe = wfpd.dataframes[source]
    dataframe = dataframe.loc[dataframe[index_column] == value]
    dataframe = dataframe.drop(index_column,1)
    return dataframe


# In[9]:


def frame_sub_json_object(dataframe,index_column,value):
    """ Essentially the same as the sub_json_object function, but can take an
        arbitrary dataframe, rather than a wfpd dataframe.
        
        Takes a dataframe and filters it on a provided value on its index_column.
        The index column is then removed, effectively providing a table
        of related data.  This table is then returned as a dataframe.
        Useful function for transforming pandas JSON friendly structures.
        
        Parameters
        ----------
        source : string
            The name of the wfpd dataframe (aka Excel sheet name)
        index_column : string
            The name of the column on the wfpd dataframe to filter on
        value : string
            The value to filter on
    """
    dataframe = dataframe.loc[dataframe[index_column] == value]
    dataframe = dataframe.drop(index_column,1)
    return dataframe


# The next two functions manipulate dataframes directly into JSON.  The _df_to_json_attribs_ takes a dataframe with a primary key_column and iterates through the values of that column and turns each row into a JSON object.  The _df_to_json_ function simply uses the standard pandas to JSON function to convert a single row into a JSON string.

# In[10]:


def df_to_json_attribs(dataframe,key_column):
    """ Iterates through each row in a dataframe that has a primary unique key
        and turns it into a JSON string
        
        Parameters
        ----------
        dataframe : pd
            The name of the wfpd dataframe (aka Excel sheet name)
        key_column : string
            The name of the column on the wfpd dataframe to filter on
    """    
    elements = len(dataframe)
    json = "{"
    count = 0
    for index, row in dataframe.iterrows():
        element = row[key_column]
        json = json + '"' + element + '":{'
        attribute_frame = dataframe.loc[dataframe[key_column] == element]
        attribute_frame = attribute_frame.drop(key_column,1)
        json = json + strip_curlies(strip_brackets(df_to_json(attribute_frame)))
        if count != (elements-1):
            json = json + "},"
        else:
            json = json + "}"
        count = count + 1
    json = json + "}"
    return json


# In[11]:


def df_to_json(dataframe):
    """Turns a pandas dataframe into a JSON string.
    
        Works file for single rows, but is a little naive in terms of transformation for
        multiple row tables

        Parameters
        ----------
        dataframe : pd, mandatory
            The pandas dataframe to turn into a JSON string
    """
    json = dataframe.to_json(orient='records')
    return json


# This function returns the available years in the model; the user can select the individual year they wish to look at and send this back to the model.

# In[12]:


def available_years():
    """Returns a JSON string of the available years in the model.
    """
    out = ""
    my_dataframe = wfpd.dataframes['population']
    list=my_dataframe.columns.values[3:]
    out = ('{ "available_years":[')
    years = len(list)
    year_count=0
    for item in list:
        out = out + (json.dumps(item))
        if year_count != (years -1):
            out = out + (",")
        else:
            out = out + ("]}")
        year_count = year_count + 1
    return out


# This function returns the data relevant to each geographic area, by geographic area.  This includes the sdoh index and the details of the primary care providers in each of the geographic areas.

# In[13]:


def geo_profile():
    """ Creates a easily addressable JSON string from the wfpd pandas dataframes that
        reports back to the front end the following data:
        
        By county/area:
            area sdoh index
            area provider supply by provider_type, for each provider/area combination
                number of providers
                growth trend
                mean_wage
    """ 
    primary_key_df_name = 'geo_area_list'
    primary_key_column = 'geo_area'
    primary_key_dataframe = wfpd.dataframes[primary_key_df_name]
    elements = len(primary_key_dataframe)
    #print (elements)
    out = "{"
    for index, row in primary_key_dataframe.iterrows():
        element = row[primary_key_column]
        out = out + '"' + element + '":{'
        out = out + strip_curlies(strip_brackets(df_to_json(sub_json_object(primary_key_df_name,primary_key_column,element)))) + ","  
        out = out + '"supply":'
        out = out + df_to_json_attribs(sub_json_object('provider_supply','provider_geo_area',element),'provider_abbr') 
        if index != elements-1:
            out = out + "},"
        else:
            out = out + "}"
    out = out + "}"
    return out


# For each provider this function provides a category based view of which services they can provide - and how suitable those services are for them to carry out.  For each service a minimum and maximum face to face time is defined.  It also provides a supply based view of each provider supply by county, including the numbers per county, the expected growth rate, mean wage and wage trends.
# 
# NB: As the following function demonstrates, constructing easily navigable JSON from pandas is a non-trivial operation.  In retrospect, the creation of the JSON string should have been done by programmatically building a Python structure that is capable of being serialised then serialising it.  For more information see [here](https://realpython.com/python-json/).

# In[14]:


def provider_profile():
    out = ""
    primary_key_df_name = 'provider_list'
    primary_key_column = 'provider_abbr'
    primary_key_dataframe = wfpd.dataframes[primary_key_df_name]
    # we will iterate the outer loop once for each provider type
    elements = len(primary_key_dataframe)
    # open the JSON string and set loop counter to zero
    out = "{"
    count = 0
    # create a loop that will iterate through each row in the provider list
    for index, row in primary_key_dataframe.iterrows():
        # extract the provider name
        element = row[primary_key_column]
        # open a JSON object that correspondes to the provider type
        out = out + '"' + element + '":{'
        # write to the JSON all the top level attributes of the provider
        out = out + strip_curlies(strip_brackets(df_to_json(sub_json_object(primary_key_df_name,primary_key_column,element))))
        # retrieve the dataframe that contains the provider/serice matrix
        pa_services = wfpd.dataframes['service_characteristics']
        # change N/A to 'no' to prevent processing errors
        pa_services = pa_services.fillna("no")
        # filter the dataframe to just those things this provider can do
        pa_services = pa_services.loc[pa_services[element] != "no"]
        # now strip the dataframe back to the information we need (including the provider column)
        pa_services = pa_services[['svc_category','svc_desc','min_f2f_time','max_f2f_time',element]]
        pa_services = pa_services.rename(columns={element:'score'})    
        #  for each of the services identified, create a unique list of the service categories they belong to
        service_category_list = pa_services['svc_category'].unique()
        # we can now work out how many categories we need to loop around
        inner_element_size = len(service_category_list)
        # now we add a second object to the provider type which contains information about the services they
        # can perform
        out = out + ","
        out = out + '"services:":['
        count3 = 0
        # we're now going to loop for every row in the service_category array
        for row2 in service_category_list:
            # take a copy of pa_services as we will be filtering it
            inner_pa_service = pa_services
            key_column = 'svc_category'
            inner_element = row2
            # define the service category name as an array
            out = out + '{"'+inner_element+'":['

            inner_pa_service = inner_pa_service.loc[inner_pa_service[key_column] == row2]
            inner_pa_service = inner_pa_service.drop(key_column,1)
            #print (inner_pa_service)
            ii_key_column = 'svc_desc'
            ii_elements = len(inner_pa_service)
            count2 = 0
            for index3, row3 in inner_pa_service.iterrows():
                ii_element = row3[ii_key_column]
                #print ("      Very inner element:" + ii_element)
                out = out + '{"' + ii_element + '":{'
                out = out + strip_curlies(strip_brackets(df_to_json(frame_sub_json_object(inner_pa_service,ii_key_column,ii_element))))
                if count2 != (ii_elements-1) :
                    out = out + "}},"
                else:
                    out = out + "}}"
                count2 = count2 + 1
            if count3 != (inner_element_size-1) :
                out = out + "]},"
            else:
                out = out + "]}"
            count3 = count3 + 1 
        out = out + "],"
        out = out + '"supply":'
        out = out + df_to_json_attribs(sub_json_object('provider_supply','provider_abbr',element),'provider_geo_area') 
        if count != elements-1:
            out = out + "},"
        else:
            out = out + "}"
        count = count + 1
    out = out + "}"
    return out


# In[15]:


def save_model():
    #out = '"' + str(pickle.dumps(wfpd.dataframes,protocol=pickle.HIGHEST_PROTOCOL)) + '"'
    
    out = str(base64.b64encode(bytes(str(pickle.dumps(wfpd.dataframes,protocol=pickle.HIGHEST_PROTOCOL)), 'utf-8')))
    
    out = '"' + out + '"'
    return out


# In[16]:


def load_model(model_id,directory):
    # global
    # retrieve file?
    # wfpd.dataframes = pickle.loads(string)
    return '"loaded"'


# In[17]:


# check to see if command is understood
if command == "available_years":
    result = available_years()
elif command == "geo_profile":
    result = geo_profile()
elif command == "provider_profile":
    result = provider_profile()
elif command == "save_model":
    result = save_model()
elif command == "load_model":
    result = load_model(value,directory)
else:
    respond(None,command,provider_type, "ERROR: Unknown function call.")
respond(str(result),str(command),str(value))

