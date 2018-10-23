#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:36:52 2018

@author: yanghy@us.ibm.com
"""

import os
os.chdir('/Users/yanghy@us.ibm.com/Desktop/test')
import pandas as pd
from pulp import *
import numpy as np
import sys
FTE_time = 60*8*365

def check_input(a):
    '''
    need to split this file 
    '''

    #===== read input
    ser_time = "ser_time_ratio.txt"
    ser_prov = "ser_prov_ratio.txt"
    ser_demand = "ser_demand_new.txt"
    ser_sutable = "ser_sutab.txt"
    supply = "supply.txt"

    ser_prov = pd.read_csv(ser_prov, sep='\t', encoding = "ISO-8859-1")
    ser_time = pd.read_csv(ser_time, sep='\t', encoding = "ISO-8859-1")
    ser_demand = pd.read_csv(ser_demand, sep='\t', encoding = "ISO-8859-1")
    ser_sutb = pd.read_csv(ser_sutable, sep='\t', encoding = "ISO-8859-1")
    supply = pd.read_csv(supply, sep='\t', encoding = "ISO-8859-1")
    provider = list(ser_prov)[4:ser_prov.shape[1]]
    supply = supply[provider]
    wage = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.3, 0.2, 0.1]
    
    # check size
    print(ser_prov.shape); print(ser_time.shape); print(ser_demand.shape); print(ser_sutb.shape); 
    
    # check service names
    
    #===== check columns 
    # it uses same services across tables
    
    #if not set(['F2F','Doc','freq']).issubset(diagnosis.columns):
    #    print( "Unable to find required column names (F2F, DOC..)")
    #    sys.exit()
    
    ser_time.columns = ['Category', 'Routine Service', 'Care Category', 'Service', 'freq', 'F2F', 'Doc', 'Physician'] 
    ser_time['Doc'] = 1; ser_time['Physician'] = 1
    ser_demand.columns = ['Category', 'Routine Service', 'Care Category', 'Service', 'Demand']
    ser_demand = ser_demand[['Category','Demand']] 

    #===== check missing information
    k = (ser_time['F2F']+ser_time['Doc']==0) | (ser_time['freq']==0) | (ser_demand['Demand']==0) | \
      np.isnan( ser_demand['Demand'] ) |  np.isnan( ser_time['freq'] ) | \
      np.isnan( ser_time['F2F'] ) | np.isnan( ser_time['Doc'] ) | np.isnan( ser_time['Physician'] )
    p = np.where( ~k )
    ser_time = ser_time.iloc[p[0], :].reset_index()
    ser_prov = ser_prov.iloc[p[0], :].reset_index()
    ser_demand = ser_demand.iloc[p[0], :].reset_index()
    ser_sutb = ser_sutb.iloc[p[0], :].reset_index()
    
    row_i = range(len(ser_prov))
    col_j = range(len(provider))
    #====== check float- expand columns 
    kk=[]
    for x in ser_prov['Physician']:
        if( x==' ' ): x = 0 
        if(  ~isinstance(x, (float, int)) > -2  ): 
            x= float("".join(x.replace('\'', '').split(","))) 
        kk.append(x)
    ser_prov['Physician'] = kk
    
    kk=[]
    for x in ser_sutb['Physician']:
        if( x==' ' ): x = 0 
        if(  ~isinstance(x, (float, int)) > -2  ): 
            x= float("".join(x.replace('\'', '').split(","))) 
        kk.append(x)
    ser_sutb['Physician'] = kk
    
    ser_prov = ser_prov.fillna(0)
    ser_sutb = ser_sutb.fillna(0)
    
    for col in provider:
        ser_prov.loc[ser_prov[col] > 0, col]  = 1
        
    for col in provider: # perhaps this will change when we have priority - move to process_input
        v = 1 - ser_sutb.loc[ser_sutb[col] > 0.5, col] 
        ser_sutb.loc[ser_sutb[col] > 0.5, col] =  v 
        ser_sutb[col] = ser_sutb[col]*2 + 0.4
        #ser_sutb.loc[ ser_sutb[col] > 1 ] = 1
        
    print( sum( ser_sutb.isna().sum() ) )
    print( sum( ser_prov.isna().sum() ) )
    
    
def process_input():
    '''
    description
    '''
    
def what_if_input_process():
    '''
    description
    '''
    
    
def call_opt_ideal(w_weight, s_weight, sutability, total_demand, ser_max, p_min, row_i, col_j, wage, provider ):
    '''
    core LP to optimize the allocation by wage or priority
    '''

    prob = LpProblem("test1", LpMinimize)
    service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)

    prob += lpSum( [ lpSum([service[(i, j)]* (wage[j]*w_weight + sutability.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
    #prob += lpSum( [ lpSum([service[(i, j)]* wage[j] for j in col_j ]) for i in row_i ] )
    # constrains
    for i in row_i:
        prob += lpSum([service[(i,j)] for j in col_j]) == total_demand.iloc[i,0] , "" # + total_demand.iloc[i,1] )
        
    #========== boundary 
    for i in row_i:
        for j in col_j:
            #prob += service[i][j] <= total_demand.iloc[i,0]
            #if( j == 0 ): 
            #    prob += service[i][j] >= total_demand.iloc[i,1]
            #    prob += service[i][j] <= total_demand.iloc[i,0] + total_demand.iloc[i,1]
            #else: 
            prob += service[(i,j)] >= 0
            prob += service[(i,j)] <= ser_max.iloc[i,j], ""
                 
    GLPK().solve(prob)
    # Solution
    
    dataset = pd.DataFrame(np.nan, row_i, col_j); 
    o = []; tt = 0 
    for v in prob.variables():
        m = v.name 
        m =  m.replace( 'service_(' , "")
        m =  m.replace( '_' , "")
        m =  m.replace( ')' , "")
        m = m.split(',')
        dataset.iloc[ int(m[0]), int(m[1]) ] = v.varValue
        tt = tt + v.varValue       
    dataset.columns = provider       
    return dataset, tt

def call_opt_current(w_weight,s_weight,sutability,total_demand,ser_max,p_min,row_i,col_j,wage,provider,supply):
    '''
    core LP to optimize the allocation by wage or priority
    '''
    supply_check = ser_max.apply(sum, axis = 0)/FTE_time < supply
    if(   (~supply_check).all(axis = 1)[0]    ):
        prob = LpProblem("test1", LpMinimize)
        service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)
    
        prob += lpSum([lpSum([service[(i, j)]*(wage[j]*w_weight + sutability.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
        #prob += lpSum( [ lpSum([service[(i, j)]* wage[j] for j in col_j ]) for i in row_i ] )
        # constrains
        for i in row_i:
            prob += lpSum([service[(i,j)] for j in col_j]) == total_demand.iloc[i,0], "" # + total_demand.iloc[i,1] )
            
        for j in col_j:
            if( (supply[provider[j]] > 0)[0] ):
                prob += lpSum([service[(i,j)] for i in row_i]) >= supply[provider[j]]*FTE_time, "" # + total_demand.iloc[i,1] )
        #========== boundary 
        for i in row_i:
            for j in col_j:
                #prob += service[i][j] <= total_demand.iloc[i,0]
                #if( j == 0 ): 
                #    prob += service[i][j] >= total_demand.iloc[i,1]
                #    prob += service[i][j] <= total_demand.iloc[i,0] + total_demand.iloc[i,1]
                #else: 
                prob += service[(i,j)] >= 0
                prob += service[(i,j)] <= ser_max.iloc[i,j], ""
                
                     
        GLPK().solve(prob)
        # Solution
        
        dataset = pd.DataFrame(np.nan, row_i, col_j); 
        o = []; tt = 0 
        for v in prob.variables():
            m = v.name 
            m =  m.replace( 'service_(' , "")
            m =  m.replace( '_' , "")
            m =  m.replace( ')' , "")
            m = m.split(',')
            dataset.iloc[ int(m[0]), int(m[1]) ] = v.varValue
            tt = tt + v.varValue       
        dataset.columns = provider     
    else: 
        dataset = np.array(provider)[ supply_check.values[0]  ]
        print("Excess providers in:",end=" "); print(','.join(dataset) )
        tt = 0
    return dataset, tt

    
def resource_allocation(Prov_comp_type, ser_prov, ser_demand, ser_sutb, provider, wage, w_weight, s_weight, provider):
    '''
    description
    '''
    # dimension
    
    n_ser = len(ser_demand)
    n_provider = len(provider)
    row_i = range( n_ser )
    col_j = range( n_provider )
    sutability = ser_sutb[provider]
    
    total_demand = pd.DataFrame(index=range(n_ser),columns=['total', 'physician'])
    for k in range( n_ser ):# service
        total_demand.iloc[k,0] = ser_demand.loc[k,'Demand'] * \
                (ser_time.loc[k,'F2F']+ser_time.loc[k,'Doc'])*ser_time.loc[k,'freq']
        # pop * time * freq
        total_demand.iloc[k,1]= ser_demand.loc[k,'Demand']*  \
                (ser_time.loc[k,'Physician'])*ser_time.loc[k,'freq']
              
    
    ser_max = pd.DataFrame(index=range(n_ser),columns=provider)
    p_min = pd.DataFrame(index=range(n_ser),columns=['min_phy'])
    
    for i in range( n_ser ):# service
        for m in provider:
            max_val  = ser_prov.loc[i, m] * total_demand.loc[i,'total'] 
            ser_max.loc[i,m] = max_val 
            if( m == 'Physician' ): 
                min_val = total_demand.loc[i,'physician'] 
                p_min.loc[i,0] = min_val
                ser_max.loc[i,m] = max_val + min_val
                    
    #====== optimization
    total_wage = []; total_sutab = []; d = pd.DataFrame(index = provider)
    for i in np.arange(0, 1.1, 0.1):
        w_weight = i; s_weight = 1- i
        if( Prov_comp_type == 'ideal'):
            dataset, tt = call_opt_ideal(w_weight, s_weight, sutability, total_demand,ser_max, p_min, row_i, col_j, wage , provider)
        if( Prov_comp_type == 'current'):
            dataset, tt = call_opt_current(w_weight,s_weight,sutability,total_demand,ser_max,p_min,row_i,col_j,wage,provider,supply)
        # calculate statistics
        if tt == 0:
            df = pd.DataFrame(np.nan, index=provider, columns = [i])
            d = pd.concat( [d, df], axis = 1) 
            total_wage.append( np.nan )
            total_sutab.append( np.nan )
        else:
            demand = dataset.apply(sum, axis = 0)/FTE_time
            d = pd.concat( [d, pd.DataFrame(data = demand, columns = [i]) ], axis = 1) 
            total_wage.append( np.round( sum(demand*wage), 0) )
            total_sutab.append( sum((dataset * sutability).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)) )
    
    d = round( d*10/5 )/2
    return total_tage, total_sutab, d        

def plotthis():
    import numpy as np
    import matplotlib.pyplot as plt

    # Create some mock data
    t = np.arange(0, 1.1, 0.1)
    data1 = np.exp(t)
    data2 = np.sin(2 * np.pi * t)

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Ratio betewwn Wage and Priority')
    ax1.set_ylabel('Wage', color=color)
    ax1.plot(t, total_wage, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Priority', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, total_sutab, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()    
    
if __name__ == '__main__': 
    pass
