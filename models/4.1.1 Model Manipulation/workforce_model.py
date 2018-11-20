
# coding: utf-8

# # Workforce Model

# This program creates a pandas dictionary from the imported Excel spreadsheet.
# 
# It can return three types of information as a result of requests from the front end:
# 
# #### Sample UI data retrival commands
# 
# * {"request_type": "available_years"}
# 
# * {"request_type": "geo_profile"}
# 
# * {"request_type": "provider_profile"}
# 
# It can also persist and 
# 
# #### Sample model save/load commands
# 
# * {"request_type": "save_model", "filename":"test_pickle"}
# 
# * {"request_type": "load_model", "filename": "test_pickle"}
# 
# #### Sample model run commands
# This program will default to running ideal staffing for the State of Utah in 2018 if no other instruction is given.
# 
# * {"request_type":"run_model"}
# 
# * {"request_type":"run_model", "geo":"State of Utah", "year":"2018", "option":"ideal_staffing", "sub_option":"all_combination"}
# 
# * {"request_type":"run_model", "geo":"Garfield County", "year":"2018", "option":"ideal_staffing", "sub_option":"all_combination"}
# 
# * {"request_type":"run_model", "geo":"State of Utah", "year":"2018", "option":"ideal_staffing", "sub_option":"wage_max", "wage_max":"20000"}
# 
# * FAIL {"request_type":"run_model", "geo":"Wayne County", "year":"2018", "option":"ideal_staffing", "sub_option":"wage_weight","wage_weight":"0.5"} FAIL
# 
# * {"request_type":"run_model", "geo":"Beaver County", "year":"2019", "option":"ideal_staffing_current", "sub_option":"all_combination"}
# 
# * {"request_type":"run_model", "geo":"Washington County", "year":"2018", "option":"ideal_staffing_current", "sub_option":"wage_max", "wage_max":"400000000"}
# 
# * FAIL {"request_type":"run_model", "geo":"Rich County", "year":"2018", "option":"ideal_staffing_current","sub_option":"wage_weight", "wage_weight":"0.75"} FAIL
# 
# * FAIL {"request_type":"run_model", "geo":"Utah County", "year":"2020", "option":"service_allocation"} FAIL
# 
# * FAIL {"request_type":"run_model", "geo":"State of Utah", "year":"2018", "option":"service_allocation"} FAIL
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

import datetime
import workforce_pandas as wfpd
import json
import sys
import pickle
import os
import pandas as pd
from allocation_ui import main
command="null"
provider_type="null"


# In[2]:


def type_of_script():
    ''' Returns jupyter if running in a notebook, otherwise returns server
    '''
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'jupyter'
    except:
        return 'server'


# Determines and stores the path for the pickle directory used to persist and retrieve models

# In[3]:


if type_of_script()=='jupyter':
    directory = r"../data/pickle/"
else:
    directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + r"/../data/pickle/")
directory


# Default values for model state, should they not be provided

# In[4]:


geo = "State of Utah"
year ="2018"
current_year = '2018'
option = "ideal_staffing"
sub_option = "all_combination"
wage_max = "null"
wage_weight = "null"
collapse_group = False


# In[5]:


wfpd.sheets


# The model takes the input of a JSON string from stdin

# In[6]:


value = "null"
command_string = input("")


# All responses are formatted and sent using the respond function below:

# In[7]:


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

# In[8]:


# parse the command line argument into a JSON object
try:
    parsed_command = json.loads(command_string)
except Exception as e:
    respond(None,command,provider_type, "ERROR: Invalid argument - not in JSON format: "+str(e))
if "request_type" in parsed_command:
    command = str(parsed_command["request_type"])
else:
    respond(None,command,provider_type, "ERROR: Invalid argument - no request_type defined")
if "filename" in parsed_command:
    filename = str(parsed_command["filename"])
if "geo" in parsed_command:
    geo = str(parsed_command["geo"])
if "year" in parsed_command:
    year = str(parsed_command["year"])
if "option" in parsed_command:
    option = str(parsed_command["option"])    
if "sub_option" in parsed_command:
    sub_option = str(parsed_command["sub_option"])
if "wage_max" in parsed_command:
    wage_max = str(parsed_command["wage_max"])
if "wage_weight" in parsed_command:
    wage_weight = str(parsed_command["wage_weight"])


# The next two functions are used to manipulate the automatically generated JSON strings as they often don't conform to the format that we require in our responses

# In[9]:


def strip_brackets(JSON_string):
    """Strips the square brackets from a JSON string

        Parameters
        ----------
        JSON_string : str, mandatory
            The JSON string to strip the leading and trailing end square brackets from
    """
    result = JSON_string.strip("[]")
    return result


# In[10]:


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

# In[11]:


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


# In[12]:


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

# In[13]:


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


# In[14]:


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


# This function returns the available years in the model; the user can select the individual year they wish to look at and send this back to the model.  At the moment, the routine deliberately restricts the return to the years 2018 to 2027.  Future enhancements may want to increase the amount of population data sent to the front end and provide a sliding window based on the current date...

# In[15]:


def available_years():
    """Returns a JSON string of the available years in the model.
    """
    out = ""
    my_dataframe = wfpd.dataframes['population']
    list=my_dataframe.columns.values[11:21]
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
    print (out)
    return


# This function returns the data relevant to each geographic area, by geographic area.  This includes the sdoh index and the details of the primary care providers in each of the geographic areas.

# In[16]:


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

# In[17]:


def provider_profile():
    """ Creates a easily addressable JSON string from the wfpd pandas dataframes that
        reports back to the front end the following data:
        
        By provider, indexed on their abbreviated name:
            the full name of the provider
            the serive categories they support
                the services that they support
                    the max f2f time
                    the min f2f time
                    where the service is on their licence to operate
            the supply profile of each provider by county
                number of FTEs
                growth trend
                mean wage
                wage trend
                
    """ 
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


# The following two functions will serialize the pandas dictionary into a file and then retrieve them.  
# 
# NB The commented out version of the save_model is less efficient, but results in a string that could be transmitted as part of a JSON string, rather than saved directly to disk.

# In[18]:


def save_model(filename):
    """Turns our dictionary of pandas dataframes into a serialised form and saves it to disk

        Parameters
        ----------
        filename : str, mandatory
            The name of the file to be used
    """
    #out = str(base64.b64encode(bytes(str(pickle.dumps(wfpd.dataframes,protocol=pickle.HIGHEST_PROTOCOL)), 'utf-8')))
    #out = '"' + out + '"'
    os.chdir(directory)
    with open(filename, 'wb') as handle:
        pickle.dump(wfpd.dataframes, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return '"Model saved."'


# In[19]:


def load_model(filename):
    """Turns pickled files back into a dictionary of pandas dataframes

        Parameters
        ----------
        filename : str, mandatory
            The name of the file to be loaded
    """
    # global
    # retrieve file?
    # wfpd.dataframes = pickle.loads(string)
    os.chdir(directory)
    with open(filename, 'rb') as handle:
        b = pickle.load(handle)
    return '"Model loaded."'


# The analytical model currently supports three optimisers.  These each have their own options.  The three optimisations are:
# 
# *Ideal Staffing* (greenfield model)
# This model will use Linear Programming to simply calculate the optimum number and type of individuals to meet the clinical needs of the target population (at a county or state level).  The analysis can be influenced by contraints that include the maximum budget and/or a tradeoff between suitability (i.e. a balanced LTO score) and wage cost.
# 
# *Ideal Staffing Current* (brownfield model)
# This model starts with an existing provider profile and uses clinical need and LTO to maximise the efficiency of the staff profile whilst minimizing staff changes.
# 
# *Service Allocation* (sharing the load)
# This model attempts to equally spread the load of services across an existing population of provider types by allocating work in such a way that the burden of care is shared as equally as it can be.  This may be useful in situation where staff numbers are difficult to change quickly.
# 
# Further details on the options are in the parameters descriptions below:

# In[20]:


def run_model(geo,year,option,sub_option,wage_max,wage_weight):
    """Runs the model optimizers based on a series of UI deltas overlaid on
        the dictionary of pandas dataframes (which represent the Excel model input) 

        Parameters
        ----------
        geo : str, mandatory
            The area on which to conduct the analysis
        year : str, mandatory
            The year to be analysed (currently not used)
        option : str, mandatory
            One of - 'ideal_staffing', 'ideal_staffing_current', 'service_allocation'
        sub_option : str, mandatory
            One of - 'all_combination', 'wage_max', 'wage_weight'
        wage_max : str, optional
            A string representation of an integer, only needed if sub_option is wage_max
        wage_weight : str, optional
            A string representation of a float between 0 and 1, only needed if sub_option is wage_weight
    """  
    # validates options and sets UI based parameters
    sub_option_value = None
    pos_option = ('ideal_staffing', 'ideal_staffing_current', 'service_allocation')
    pos_sub_option = ("all_combination", "wage_max", "wage_weight")
    if ( (option not in pos_option) | (sub_option not in pos_sub_option) ):
        respond(None,command,"null", "ERROR: unknown model calculation options")
    if sub_option == "wage_max":
        sub_option_value = int(wage_max)
    elif sub_option == "wage_weight":
        sub_option_value = float(wage_weight)
    
    # gets the latest version of the dictionary dataframes to pass into the 
    # optimizer model.  This ensures that any deltas processed from the UI are taken
    # into account
    pop_chronic_trend = wfpd.dataframes['pop_chronic_trend']
    pop_chronic_prev = wfpd.dataframes['pop_chronic_prev']
    chron_care_freq = wfpd.dataframes['chron_care_freq']
    geo_area = wfpd.dataframes['geo_area_list']
    service_characteristics = wfpd.dataframes['service_characteristics']
    pop_acute_need = wfpd.dataframes['pop_acute_need']
    population = wfpd.dataframes['population']
    provider_supply = wfpd.dataframes['provider_supply']
    pop_prev_need = wfpd.dataframes['pop_prev_need']
    provider_list = wfpd.dataframes['provider_list']
    encounter_detail = wfpd.dataframes['encounter_detail']
    overhead_work = wfpd.dataframes['overhead_work']
    
    # additional parameters used to call the model but not currently
    # in the spreadsheet or the user interface
    
    sut_target = 0.8 # sutability target 0.8 is ideal status
    FTE_time = 60*2080 # perhaps default 124,800
    
    # call the model
    out = main(geo, year, current_year, option, sub_option, sub_option_value, sut_target,  collapse_group, FTE_time, 
         pop_chronic_trend, pop_chronic_prev, chron_care_freq, geo_area, service_characteristics, 
         pop_acute_need, population, provider_supply , pop_prev_need , provider_list , encounter_detail, overhead_work)
    
    # return the results dictionary
    return json.loads(out)


# The result returned from the model is a complex structure, so this function breaks it down into name/value pairs and then dumps them to a JSON string for return to the end user
# 
# ###NOTE
# Currently the detailed results part of the results dictionary are not returned as they are not human readable.  When the UI can be extended with the detailed results, then it is suggested that they are returned for visualisation.  At the moment, the wage, suitability and FTE profiles by provider are returned.

# In[21]:


def process_result(result):
    """Simplifies the results of the optimizer models into a simple JSON string.  Currently only three parts of the
        optimizer model results are supported.  The detail is too hard for a human to read as a JSON string and
        not yet supported by the UI...

        Parameters
        ----------
        result : dict, mandatory
            The results dictionary, which has four parts (allocation, total wage, suitability and detailed results)
    """  
    if isinstance(result, str):
        respond(None,command,provider_type, "ERROR: No possible optimization.")
        
    if 'allocation' in result:
        allocation = (result['allocation'])
        allocation.rename(columns={'provider_abbr':'name', 0: 'FTE'}, inplace=True)
        allocation['total_wage'] = result['total_wage']
        allocation['total_sutab'] = result['total_sutab']
        results_dict ={}
        results_dict = allocation.to_dict()
    else:
        results_dict = next(iter(result.values()))
    
    
    
    
    #total_wage = result['total_wage']
    #total_sutab = result['total_sutab']
    #results_dict['total_wage'] = total_wage
    #results_dict['total_sutab'] = total_sutab
    
    out = json.dumps(results_dict)
    return out


# This continues the main processing routine of the program and farms out the different request types out to varying functions.  Each of them returns a result as a JSON string that is then returned to the caller via a respond message

# In[22]:


if command == "available_years":
    result = available_years() # respond to UI request for trending/trend information
elif command == "geo_profile":  
    result = geo_profile() # respond to UI request for geographic area information
elif command == "provider_profile": 
    result = provider_profile() # respond to UI request for provider information
elif command == "save_model":
    result = save_model(filename) # restore/unpic#kle the current dataframe dictionary
elif command == "load_model":
    result = load_model(filename) # pickle the current dataframe dictionary
elif command == "run_model": 
    result = run_model(geo,year,option,sub_option,wage_max,wage_weight) # run the optimizer
    
    with open("/workdir/model.txt", mode='a+') as file:
        file.write('%s - %s\n' % 
               (datetime.datetime.now(), result))
        file.close()
    result = process_result(result) # process complex result into a JSON string
else:
    respond(None,command,provider_type, "ERROR: Unknown function call.")
respond(str(result),str(command),str(value))

