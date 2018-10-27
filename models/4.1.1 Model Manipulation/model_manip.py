
# coding: utf-8

# # 4.1.1. Model Manipulation

# In[1]:


# coding: utf-8
#
# This is the bare bones of the component 4.1.1 Model Manipulation
# It receives a JSON formatted instruction via the command line in
# the form:
#
# python model_manip.py
#
# Then send a string similar to the following in via std in:
# {"request_type": "provider_profile", "value": "Psych"}
# {"request_type": "provider_list", "value": "all"}
# {"request_type": "provider_details", "value": "all"}
#
#
# It responds via std out with a JSON string that includes the originating call
# and an additional response string (which in itself is a JSON string)
#
# Originally developed in Jupyter Notebook, it is converted to standard Python via :
#  jupyter nbconvert --to script 4_1_1_Model_Manipulation.ipynb
#

import pandas as pd
import json
import sys
import os

#directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../test/data_input_component_CSV/")
directory = "../test/data_input_component_CSV/"

command="null"
provider_type="null"


# In[2]:


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
    response = '{"request":{"request_type":"' + verb + '", "value": "' + object + '"},"response":' + response_msg + '}'
    print (response)
    sys.exit(0)


# In[3]:


def strip_brackets(JSON_string):
    """Strips the brackets

        Parameters
        ----------
        JSON_string : str, mandatory
            The JSON string to strip the leading and trailing end brackets from
    """
    result = JSON_string.strip("[]")
    return result


# In[4]:


class ProviderClass:        
    def get_provider_list(self, provider_list):
        # retrieve list of providers
        provider_list = provider_list.loc[provider_list['provider_abbr'].notnull()]
        provider_list = provider_list[['provider_name','provider_abbr']]
        out = '{"provider":' + strip_brackets(provider_list.to_json(orient='records')) + '}'
        return out
    def get_provider_profile(self,provider_type,provider_list,provider_supply,acute_service_prov_priority):
        # First we create the header for the provider type with their full title and wage
        provider_head_profile = provider_list.loc[provider_list['provider_abbr'] == provider_type]
        # Then we check to see if the requested provider type is in the current provider list
        if len(provider_head_profile.index) != 1:
            respond(None,command,provider_type, "ERROR: Provider type is not known.")
        # Second, we want to create the geographic profile of the provider type
        # First we reduce the data frame to the three provider columns
        provider_supply = provider_supply[['provider_abbr','provider_county','provider_num']]
        # Then we reduce the data frame to just the rows relevant to the requested provider type
        provider_supply1 = provider_supply.loc[provider_supply['provider_abbr'] == provider_type]
        # Finally we strip out the provider abbrevialtion column as it is now redundant
        provider_supply_profile = provider_supply1[['provider_county','provider_num']]
        # For the final part of the profile, we change the provider type column in the service
        # to provider mapping matrix to the priority column that we will output
        acute_service_prov_priority.rename(columns={provider_type: 'priority'}, inplace=True)
        # We then order the services from the most suitable for that provider down to the
        # ones that they are not allowed to perform
        acute_service_prov_priority=acute_service_prov_priority.sort_values(by=['priority','acute_encounter','acute_cateogry','acute_service'])
        # We then reduce the output of the dataframe to the needed four columns
        profile_services = acute_service_prov_priority[['priority','acute_encounter','acute_cateogry','acute_service']]
        profile_services.head(10)
        out = '{"provider":' + strip_brackets(provider_head_profile.to_json(orient='records')) + ','
        out = out + '"supply":' + provider_supply_profile.to_json(orient='records') + ','
        out = out + '"services":' + profile_services.to_json(orient='records') + '}'
        return out
    def get_all_providers(self,provider_list,provider_supply,acute_service_prov_priority):
        provider_list = provider_list.loc[provider_list['provider_abbr'].notnull()]
        provider_list = provider_list[['provider_name','provider_abbr']]
        provider_supply = provider_supply[['provider_abbr','provider_county','provider_num']]
        acute_service_prov_priority=acute_service_prov_priority.dropna(how='all',axis=1)
        out = '{"provider":' + provider_list.to_json(orient='records') + ','
        out = out + '"supply":' + provider_supply.to_json(orient='records') + ','
        out = out + '"services":' + acute_service_prov_priority.to_json(orient='records') + '}'
        return out


# In[5]:


#    def get_all():
#        # get all provider data
#    def change_state():
#        # update provider data#


# In[6]:


# Next we import the relevant sheets from the Data Input Component (to begin with only three)
try:
    provider_list = pd.read_csv(directory + "/provider_list.csv")
    provider_supply = pd.read_csv(directory + "/provider_supply.csv")
    acute_service_prov_priority = pd.read_csv(directory + "/acute_service_prov_priority.csv")
    geo_area_list = pd.read_csv(directory + "/geo_area_list.csv")
    population = pd.read_csv(directory + "/population.csv")
except Exception as e:
    respond(None,command,provider_type, "ERROR: Could not read input files."+str(e))


# In[7]:


command_string = input("")


# In[8]:


provider=ProviderClass()
provider


# In[9]:


# parse the command line argument into a JSON object
try:
    parsed_command = json.loads(command_string)
    value = str(parsed_command["value"])
    command = str(parsed_command["request_type"])
except Exception as e:
    respond(None,command,provider_type, "ERROR: Could not parse argument: "+str(e))
command


# In[10]:


# check to see if command is understood
if command == "provider_profile":
    result = provider.get_provider_profile(value,provider_list,provider_supply,acute_service_prov_priority)
elif command == "provider_list":
    result = provider.get_provider_list(provider_list)
elif command == "provider_details":
    result = provider.get_all_providers(provider_list,provider_supply,acute_service_prov_priority)   
else:
    respond(None,command,provider_type, "ERROR: Unknown function call.")
respond(result,command,value)


# class GeographicArea:
#     def __init__(self):
#         # do stuff
#     def get_area_list():
#         # retrieve list of counties
#     def get_county_data(county):
#         # get county data
#     def get_all():
#         # get all data
#     def change_state():
#         # update geo data
#     def __change_wage(county,provider)
#         # private function to change wage in pandas
#         
