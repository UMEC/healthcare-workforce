#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10/18/2018 test code for model_as_is

@author: yanghy@us.ibm.com
"""

import pandas as pd
import numpy as np

def calculate_demsuf(ser_time_name, ser_prov_name,  ser_demand_name, arch_prov_name, arch_pt_name, supply_name, assign_name):
    '''
    description
    
    ser_time_name ='ser_time.csv'; 
    ser_prov_name='ser_prov.csv'; 
    ser_demand_name ='ser_demand.csv';
    arch_prov_name = 'arch_prov.csv'
    arch_pt_name = 'arch_pt.csv';
    supply_name = 'supply.csv';
    assign_name = 'assign.csv'
    '''
    
    # get input
    ser_time = pd.read_csv(ser_time_name)
    ser_prov = pd.read_csv(ser_prov_name)
    ser_demand = pd.read_csv(ser_demand_name)
    arch_prov = pd.read_csv(arch_prov_name)
    arch_pt = pd.read_csv(arch_pt_name)
    supply = pd.read_csv(supply_name)
    assign = pd.read_csv(assign_name)
    
    ser_time1 = pd.isnull(ser_time).apply(sum, axis = 1)
    ser_demand1 = pd.isnull(ser_demand).apply(sum, axis = 1)
    
    # assume these are OK. Otherwise...
    
    arch_pt['Patients'] = arch_pt['Patients']/sum(arch_pt['Patients'])
    #arch_pt1 = pd.isnull(arch_pt).apply(sum, axis = 1)
    #if sum(arch_pt1) >0: 
    #    print("Invalid file")
    #    import sys
    #    exit()
    
    # other variables null = 0 
    
    fail_ser_time = None; fail_ser_demand = None; 
    if( sum(ser_time1)>0 ): fail_ser_time = ser_time.iloc[ np.where( ser_time1==1)[0], :]
    if( sum(ser_demand1)>0 ): fail_ser_demand = ser_demand.iloc[ np.where( ser_demand1==1)[0], :]
    
    #fail_arch_pt  = None; fail_supply = None; fail_assign = None
    #if( sum(arch_pt1)>0 ): fail_arch_pt = arch_pt.iloc[ np.where( arch_pt1==1)[0], :]
    #if( sum(supply1)>0 ): fail_supply = supply.iloc[ np.where( supply1==1)[0], :]
    #if( sum(assign1)>0 ): fail_assign = assign.iloc[ np.where( assign1==1)[0], :]
    
    k = (ser_time1 == 1 ) | (ser_demand1==1) 
    p = np.where( ~k )
    
    ser_time = ser_time.iloc[p[0], :].reset_index()
    ser_prov = ser_prov.iloc[p[0], :].reset_index()
    ser_demand = ser_demand.iloc[p[0], :].reset_index()
    
    
    # dimension
    n_arch = len(arch_pt)
    n_ser = len(ser_demand)
    n_provider = arch_prov.shape[1] - 1
    provider = list(arch_prov)[1:(n_provider+1)]
    supply = supply[provider]
    
    
    total_demand = pd.DataFrame(index=range(n_ser  * n_arch),columns=provider)
    for j in range( n_arch ): 
        for i in range( n_ser ):# service
            k = j* n_ser + i 
            #total_demand.rename(index={k:row_i}, inplace=True)
            f2f = ser_demand.loc[i,'Demand'] * arch_pt.loc[j,'Patients'] * \
                (ser_time.loc[i,'F2F']+ser_time.loc[i,'Doc'])*ser_time.loc[i,'freq']
            phytime= ser_demand.loc[i,'Demand']* arch_pt.loc[j,'Patients'] * \
                (ser_time.loc[i,'Physician'])*ser_time.loc[i,'freq']
            
            total_demand.loc[k,: ] = assign.loc[k, :]* f2f
            total_demand.loc[k,'Physician'] = assign.loc[k, 'Physician']* f2f + phytime
    
    totaldemand = total_demand.apply(np.nansum, axis = 0)
    dmd_ser =  pd.concat([totaldemand, supply.T*365*8.], axis = 1)
    dmd_ser.columns =['demand', 'supply']
    return total_demand, dmd_ser, fail_ser_time, fail_ser_demand 

if __name__ == '__main__': 
    pass
 