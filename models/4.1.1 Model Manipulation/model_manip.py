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
#
# It responds via std out with a JSON string that includes the originating call
# and an additional response string (which in itself is a JSON string)

import pandas as pd
import json
import sys
import os

#scriptpath = os.path.realpath(__file__)
#print("Script path is : " + scriptpath)

directory = "../test/Data Input Component CSV/"

command="null"
provider_type="null"

def respond(response_msg,verb,object):
    """Prints a JSON formatted service response to std out and exits the program

        Parameters
        ----------
        response_msg : str, mandatory
            The message included in the response attribute of the JSON out
        verb : str, mandatory
            The command that was received (if any)
        object: str, mandatory
            The target for the command that was received (if any)
    """
    response = '{"request":[{"request_type":"' + verb + '", "value": "' + object + '"}],"response":[' + response_msg + ']}'
    print (response)
    sys.exit(0)

# check to see if the correct number of command line arguments have been received
#if len(sys.argv) != 2 :
#    respond("ERROR: Incorrect number of arguments.","null","null")
command_string = input("")

# parse the command line argument into a JSON object
try:
    parsed_command = json.loads(command_string)
    provider_type = str(parsed_command["value"])
    command = str(parsed_command["request_type"])
    command
    provider_type
except Exception as e:
    respond("ERROR: Could not parse argument: " + e,command,provider_type)

# check to see if command is understood
if command != "provider_profile":
    respond("ERROR: Unknown function call.",command,provider_type)

# Next we import the relevant sheets from the Data Input Component (to begin with only three)

try:
    provider_list = pd.read_csv(directory + "provider_list.csv")
    provider_supply = pd.read_csv(directory + "provider_supply.csv")
    acute_service_prov_priority = pd.read_csv(directory + "acute_service_prov_priority.csv")
except:
    respond("ERROR: Could not read input files.",command,provider_type)

provider_list.head(5)

# First we create the header for the provider type with their full title and wage
provider_head_profile = provider_list.loc[provider_list['provider_abbr'] == provider_type]
# Then we check to see if the requested provider type is in the current provider list
if len(provider_head_profile.index) != 1:
    respond("ERROR: Provider type is not known.",command,provider_type)
provider_head_profile

provider_supply.head(5)

# Second, we want to create the geographic profile of the provider type
# First we reduce the data frame to the three provider columns
provider_supply = provider_supply[['provider_abbr','provider_county','provider_num']]
# Then we reduce the data frame to just the rows relevant to the requested provider type
provider_supply1 = provider_supply.loc[provider_supply['provider_abbr'] == provider_type]
# Finally we strip out the provider abbrevialtion column as it is now redundant
provider_supply_profile = provider_supply1[['provider_county','provider_num']]

provider_supply_profile.head(5)

acute_service_prov_priority.head(5)

# For the final part of the profile, we change the provider type column in the service
# to provider mapping matrix to the priority column that we will output
acute_service_prov_priority.rename(columns={provider_type: 'priority'}, inplace=True)
# We then order the services from the most suitable for that provider down to the
# ones that they are not allowed to perform
acute_service_prov_priority=acute_service_prov_priority.sort_values(by=['priority','acute_encounter','acute_cateogry','acute_service'])
# We then reduce the output of the dataframe to the needed four columns
profile_services = acute_service_prov_priority[['priority','acute_encounter','acute_cateogry','acute_service']]

profile_services.head(10)

def strip_brackets(JSON_string):
    """Strips the brackets

        Parameters
        ----------
        JSON_string : str, mandatory
            The JSON string to strip the leading and trailing end brackets from
    """
    result = JSON_string.strip("[]")
    return result

# Finally we assemble the final JSON output from the three separate bits of the profile
out = '{"header":' + provider_head_profile.to_json(orient='records') + ','
out = out + '"supply":' + provider_supply_profile.to_json(orient='records') + ','
out = out + '"services":' + profile_services.to_json(orient='records') + '}'
# And issue them via std out and exit
#respond(out,command,provider_type)
respond(out,command,provider_type)
