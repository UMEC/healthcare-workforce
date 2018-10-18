#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10/18/2018 
test code for model_as_is_api

@author: yanghy@us.ibm.com
"""
import os
os.chdir('/Users/yanghy@us.ibm.com/Documents/microblog/DiseaseStaging/')
from flask import Flask,  jsonify
from flask_restplus import Resource, Api
from model_as_is_v0 import calculate_demsuf
import pandas as pd
   
app = Flask(__name__)

api = Api(
   app, 
   version='1.0', 
   title='calculate as is ',
   description='API to get supply demand')

ns = api.namespace('ModelAsIs', 
   description='API to get ..')

@api.route("/retrain/<string:ser_time_name>/<string:ser_prov_name>/<string:ser_demand_name>/<string:arch_prov_name>/<string:arch_pt_name>/<string:supply_name>/<string:assign_name>")
#@api.doc(params={'ser_time_name,':'Name of .csv format input file ser_time, with  columns ...'})
#@api.doc(params={'ser_prov_name,':'Name of .csv format input file ser_prov, with  columns ...'})
#@api.doc(params={'ser_demand_name,':'Name of .csv format input file ser_demand, with  columns ...'})
#@api.doc(params={'arch_prov_name,':'Name of .csv format input file arch_prov, with  columns ...'})
#@api.doc(params={'arch_pt_name,':'Name of .csv format input file arch_pt, with  columns ...'})
#@api.doc(params={'supply_name,':'Name of .csv format input file supply_name, with  columns ...'})
#@api.doc(params={'assign_name,':'Name of .csv format input file assign_name, with  columns ...'})

class DMcompApi(Resource):
    @api.response(200, 'Success!')

    def post(self, ser_time_name, ser_prov_name,  ser_demand_name, arch_prov_name, arch_pt_name, supply_name, assign_name): 
        
        total_demand, dmd_ser, fail_ser_time, fail_ser_demand  = calculate_demsuf(ser_time_name, ser_prov_name,  ser_demand_name, arch_prov_name, arch_pt_name, supply_name, assign_name)
        result = {}
        result['total_demand'] = total_demand.to_json()
        result['dmd_ser'] = dmd_ser.to_json()
        result['fail_ser_time'] = fail_ser_time.to_json()
        result['fail_ser_demand'] = fail_ser_demand.to_json()
        
        try:
            return result
        except Exception as e:
            return jsonify("{'error':'An error occurred:\n" + str(e)+"'}")


if __name__ == '__main__':
    app.run()
    
