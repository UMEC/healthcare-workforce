#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 20:28:30 2018

@author: yanghy@us.ibm.com
pop = pd.read_csv('population.csv')
provider_list = pd.read_csv('provider_list.csv') # doc_per
preventive_service_demand = pd.read_csv('preventive_service_demand.csv')
acute_service_demand = pd.read_csv('acute_service_demand.csv')
chronic_service_demand = pd.read_csv('chronic_service_demand.csv')	
acute_service_prov_priority = pd.read_csv('acute_service_prov_priority.csv')
chronic_service_prov_priority = pd.read_csv('chronic_service_prov_priority.csv')
prev_service_prov_priority = pd.read_csv('prev_service_prov_priority.csv')
acute_service_prov_priority = pd.read_csv('acute_service_prov_priority.csv')
provider_supply = pd.read_csv('provider_supply.csv')

"""
import pandas as pd
from pulp import *
import numpy as np
import sys
from numpy import dot
from cvxopt import matrix, solvers


def main(geo, year, option, sub_option, sub_option_value, sut_target, sdoh_target, FTE_time, sdoh_score, pop_chronic_trend,  
         pop_chronic_prev, chron_care_freq, geo_area, service_characteristics, pop_acute_need , 
         population, provider_supply , pop_prev_need , provider_list , encounter_detail, overhead_work):
             
    pos_option = ('idal_staffing', 'ideal_staffing_current', 'service_allocation')
    pos_sub_option = ("all_combination", "wage_max", "wage_weight")
    # input checking
    if ( (option not in pos_option) | (sub_option not in pos_sub_option) ):
        print("Invalid option. Option should be one of [all_combination, wage_max, wage_weight]. \
              \n Will calculate using default option, i.e. wage_weight = 1")
        sub_option_value = 1
        option = 'ideal_staffing' 
        pos_sub_option = "wage_weight"
        
    if (sub_option == "all_combination") | (option == 'service_allocation'): 
        w_weight = None
        s_weight = None
        
    if ( sub_option == 'wage_weight' ):
        w_weight = sub_option_value
        s_weight = 1-w_weight
    print("Creating Input File")
    
    wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name = \
    input_create(geo, year, sut_target, sdoh_target, sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need , population, provider_supply , pop_prev_need , 
             provider_list , encounter_detail, overhead_work )
    
    print("run optimization")
    service_group = False
    total_wage, total_sutab, d = resource_allocation(option, wage, ser_prov, demand, supply, overhead_work, 
                   provider_list, service_name, service_group, w_weight, s_weight, FTE_time)
   
    n = len(total_wage)
    if( w_weight == None):
        weight = pd.DataFrame(np.arange(0, 1.1, 0.1), index=np.arange(n))
        total_wage = pd.DataFrame(total_wage, index=np.arange(n))
        total_sutab = pd.DataFrame(total_sutab, index=np.arange(n))
        d1 = pd.DataFrame(d.T) 
        d1.index = range(n)
        out = pd.concat([weight,  total_wage, total_sutab,d1], axis =1)
        m = provider_list['provider_abbr'].values
        m1 = ['weight','total_Wage','total_sutab']
        m1.extend( m.tolist() )
        out.columns = m1
    else:
        weight = pd.DataFrame( {'weight' : w_weight} , index=[0])
        total_wage = pd.DataFrame( total_wage,  index=np.arange(n))
        total_sutab = pd.DataFrame(total_sutab, index=np.arange(n))
        d1 = pd.DataFrame(d.T) 
        d1.index = range(n)
        out = pd.concat([weight,  total_wage, total_sutab,d1], axis =1)
        m = provider_list['provider_abbr'].values
        m1 = ['weight','total_Wage','total_sutab']
        m1.extend( m.tolist() )
        out.columns = m1
    return out
    
    
def input_create(geo, year, sut_target, sdoh_target, sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need , population, provider_supply , pop_prev_need , 
             provider_list , encounter_detail, overhead_work):
            
    # assumption: user set county/geography 
    # order is the preserved
    # if(  ~isinstance(x, (float, int)) > -2  ):
    
    # preventive care demand
     
    #pop = pd.read_csv('population.csv')
    
    population = population.loc[ population['pop_geo_area'] == geo, : ]
    population = population[ ['pop_sex','pop_age',year] ] 
    total_pop = population[year].sum()

    # preventive demand
    prev_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Preventive',:]
    prev_df = pd.merge(prev_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])
    p_demand = []
    for i in range(len(prev_df)): # demand = rate_per_encounter * freq * n of population * time
        tmpid = prev_df.loc[i,'encounter_type']
        tmp = pop_prev_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
        freq = tmp[ tmpid ].astype(int)
        s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
        s = s.loc[ tmp[tmpid] > 0 ]; e = e.loc[ tmp[tmpid] > 0 ]; g = g.loc[ tmp[tmpid] > 0 ]# total population need service
        freq = freq.loc[ tmp[tmpid] > 0 ];
        t_demand = 0
        for j in range( sum( tmp[tmpid] > 0 )): # won's have BOTH
            if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
            if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
            t_demand = t_demand + r*freq.iloc[j]
        p_demand.append(t_demand) # frequency * population 
    f2f = prev_df['max_f2f_time']
    if( any(sdoh_score  < sdoh_target)  ): f2f = prev_df['min_f2f_time']
    
    prev_demand = prev_df['rate_per_encounter'] * f2f * p_demand
    prev_service_name  = prev_df[['encounter_category','svc_category']]
    prev_ser_prv = prev_df[ provider_list['provider_abbr'] ]
    
    # acute demand
    acute_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Acute',:]
    acute_df = pd.merge(acute_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])

    a_demand = []
    for i in range(len(acute_df)): # demand = rate_per_encounter * freq * n of population * time
        tmpid = acute_df.loc[i,'encounter_type']
        tmp = pop_acute_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
        freq = tmp[ tmpid ].astype(float)
        s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
        s = s.loc[ tmp[tmpid] > 0 ]; e = e.loc[ tmp[tmpid] > 0 ]; g = g.loc[ tmp[tmpid] > 0 ]# total population need service
        freq = freq.loc[ tmp[tmpid] > 0 ];
        t_demand = 0
        for j in range( sum( tmp[tmpid] > 0 )): # won's have BOTH
            if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
            if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
            t_demand = t_demand + r *freq.iloc[j]
        a_demand.append(t_demand) 
        # total demand
    f2f = acute_df['max_f2f_time']
    if( any(sdoh_score  < sdoh_target)  ): f2f = acute_df['min_f2f_time']
    
    acute_demand = acute_df['rate_per_encounter'] * f2f * a_demand
    acute_service_name  = acute_df[['encounter_category','svc_category']]
    acute_ser_prv = acute_df[ provider_list['provider_abbr'] ]
    
    # chronic demand
    chro_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Chronic',:]
    chro_df = pd.merge(chro_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc']) 
    c_demand = []
    for i in range(len(chro_df)): # demand = rate_per_encounter * freq * n of population * time
        tmpid = chro_df.loc[i,'encounter_type']
        freq = chron_care_freq.loc[ chron_care_freq[ tmpid ] > 0, ['chron_cond_abbr', tmpid]]
        t_demand = 0
        if( len(freq) > 0 ):
            if( len(freq) > 1 ):
                prev_freq = pop_chronic_prev[freq['chron_cond_abbr']].apply(lambda x: sum( (freq.iloc[:,1].values) * x.values ), axis = 1)
                prev_freq = prev_freq.values
            else:
                prev_freq = pop_chronic_prev[ freq['chron_cond_abbr'] ]*freq.iloc[0,1].astype(float)
                prev_freq = prev_freq.values
                prev_freq = np.squeeze(prev_freq)

            tmp = pop_chronic_prev[ ['pop_min_age','pop_max_age','pop_sex' ] ]
            #tmp = tmp.iloc[ np.where(prev_freq > 0)[0],:]
            s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
            #prev_freq = prev_freq[ prev_freq > 0 ];
            for j in np.where(prev_freq > 0)[0]: 
                if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                  (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
                if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                  (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
                t_demand = t_demand + r *prev_freq[j]
        
        c_demand.append(t_demand) 
        # total demand
    f2f = chro_df['max_f2f_time']
    if( any(sdoh_score  < sdoh_target)  ): f2f = chro_df['min_f2f_time']
    
    chronic_demand = chro_df['rate_per_encounter'] * f2f * c_demand
    chronic_service_name  = chro_df[['encounter_category','svc_category']]
    chronic_ser_prv = chro_df[ provider_list['provider_abbr'] ]
            
    demand = pd.concat( [prev_demand, acute_demand, chronic_demand ] ).reset_index( drop=True )
    demand = demand.to_frame('demand') # demand
    ser_prov = pd.concat( [prev_ser_prv, acute_ser_prv, chronic_ser_prv ] ).reset_index( drop=True )
    service_name = pd.concat( [prev_service_name, acute_service_name, chronic_service_name] ).reset_index( drop=True )
    
    supply = provider_supply.loc[ provider_supply['provider_geo_area'] == geo, : ]
    supply = supply[  ['provider_abbr','provider_num','provider_mean_wage'] ] 
    supply.index = supply['provider_abbr']
    wage = supply['provider_mean_wage']/sum(supply['provider_mean_wage'])

    
    for col in provider_list['provider_abbr']: 
        ser_prov[col] = ser_prov[col].replace('^\s*$', np.nan, regex=True).astype(float)
        v = 2*sut_target - ser_prov.loc[ser_prov[col] > sut_target, col] 
        ser_prov.loc[ ser_prov[col] > sut_target, col ] =  v 
        ser_prov[col] = 1- ser_prov[col]/sut_target
    # ser_prov optimized by sut_target
   
    # need to remove NA
    ser_prov = ser_prov.fillna(1)
    supply = supply.fillna(0)
    overhead_work = overhead_work.fillna(0) 
    wage = wage.fillna(0)
    
    k = (demand==0) | (np.isnan(demand)) 
    p = np.where( ~k )
    ser_prov = ser_prov.iloc[p[0], :].reset_index( drop=True )
    demand = demand.iloc[p[0]].reset_index( drop=True )
    service_name = service_name.iloc[p[0], :].reset_index(drop=True  )
    
    wage = wage.loc[ provider_list['provider_abbr'] ]
    ser_prov = ser_prov[ provider_list['provider_abbr']  ]
    supply = supply.loc[ provider_list['provider_abbr'] ]
    #overhead_work = overhead_work[ provider_list['provider_abbr']  ]
    return wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name
       
def resource_allocation(option, wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name, 
                        service_group, w_weight, s_weight, FTE_time):
    '''
    description
    '''
    # dimension
    n_ser = len(demand)
    n_provider = len(provider_list)
    col_j = range(n_provider)
    row_i = range(n_ser)
    
    #================== get pattern 
    if(service_group == True):
        k = service_name['encounter_category']; 
        k1 = service_name['svc_category']
        k2 = k + k1
        p = ser_prov.apply(lambda x: ''.join( ((x > 0)*1).astype('str') ), axis = 1)
        k2 = k2 + p
        df = pd.concat([k, k1, k2], axis = 1); df.columns = ['d_type','category','comb']
        k1 = df.groupby(["comb"]).size(); n_mem = len(k1) 

        # create assignment 
        ser_prov_mem = pd.DataFrame(index=range( len(ser_prov) ),columns=['mem'])
        for i in range( len(k1) ):
            ser_prov_mem.loc[ df['comb'] == k1.keys()[i] ] = i        
 
        # total Demand    
        demand_mem = pd.DataFrame(index=range(n_mem),columns=['demand'])
        for k1 in range(n_mem):
            g = demand.loc[ ser_prov_mem['mem'] == k1 , :].apply(sum, axis = 0)
            demand_mem.iloc[k1,:] = g
        

    ser_max = pd.DataFrame(index=range(n_ser),columns=provider_list['provider_abbr'])
    for i in range( n_ser ):# service
        for m in provider_list['provider_abbr']:
            max_val  = (ser_prov.loc[i, m] < 1 ) * demand.loc[i,'demand'] 
            ser_max.loc[i,m] = max_val 
                      
    #====== optimization
    total_wage = []; total_sutab = []; 
    d = pd.DataFrame(index = provider_list['provider_abbr'])
    if w_weight == None:
        for i in np.arange(0, 1.1, 0.1):
            w_weight = i; s_weight = 1- i
            if( option == 'ideal_staffing'):
                dataset, tt = call_opt_ideal(w_weight, s_weight, wage, ser_prov, demand, ser_max, row_i, col_j,FTE_time)
            if( option == 'ideal_staffing_current'):
                dataset, tt = call_opt_current(w_weight, s_weight, wage, ser_prov, demand, supply, ser_max, row_i, col_j,FTE_time)
            # calculate statistics
            if tt == 0:
                df = pd.DataFrame(np.nan, index=provider_list['provider_abbr'], columns = [i])
                d = pd.concat( [ d, df], axis = 1)   
                total_wage.append( np.nan )
                total_sutab.append( np.nan )
            else:
                dataset.columns = provider_list['provider_abbr']
                df = dataset.apply(sum, axis = 0)/FTE_time
                d = pd.concat( [ d, df], axis = 1) 
                total_wage.append( np.round( sum(df*supply['provider_mean_wage']), 0) )
                total_sutab.append( sum((dataset * ser_prov).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)) )
                
    else:
        if( option == 'ideal_staffing'):
            dataset, tt = call_opt_ideal(w_weight, s_weight, wage, ser_prov, demand, ser_max,row_i, col_j,FTE_time)
        if( option == 'ideal_staffing_current'):
            dataset, tt = call_opt_current(w_weight, s_weight, wage, ser_prov, demand, ser_max, supply, row_i, col_j,FTE_time)
        # calculate statistics
        if tt == 0:
            df = pd.DataFrame(np.nan, index=provider_list['provider_abbr'], columns = [i])
            d = pd.concat( [ d, df], axis = 1)   
            total_wage.append( np.nan )
            total_sutab.append( np.nan )
        else:
            dataset.columns = provider_list['provider_abbr']
            df = dataset.apply(sum, axis = 0)/FTE_time
            d = pd.concat( [ d, df], axis = 1) 
            total_wage.append( np.round( sum(df*supply['provider_mean_wage']), 0) )
            total_sutab.append( sum((dataset * ser_prov).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)) )
    
    d = round( d*10/5 )/2
    return total_wage, total_sutab, d        

def call_opt_ideal_maxbudget(max_wage, wage, ser_prov, demand, ser_max, row_i, col_j, FTE_time ):
    '''
    core LP to optimize the allocation by wage or priority --- find something that using grid search
    '''
    # calculate minimum wage 
    w = supply['provider_mean_wage']
    prob = LpProblem("test1", LpMinimize)
    service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)
    # objective function
    w_weight = 1; s_weight = 0
    #prob += lpSum( [ lpSum([service[(i, j)]* (wage.iloc[j]*w_weight + ser_prov.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
    prob += lpSum( [ lpSum([service[(i, j)]* w.iloc[j] for j in col_j ]) for i in row_i ] )
    # constrains - each service sum = total demand
    for i in row_i:
        prob += lpSum([service[(i,j)] for j in col_j]) == demand.iloc[i,0] , "" 
    GLPK().solve(prob)
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
    # minimum wage
    dataset.columns = supply['provider_abbr']
    df = dataset.apply(sum, axis = 0)/FTE_time
    iminwage = np.round( sum(df*w), 0)
    if( max_wage < minwage ): 
        print('Budget should be bigger than $'+ iminwage.astype(str))
    else:
        # calculate maximum sutability 
        max_wage = iminwage + 10000
        prob = LpProblem("test1", LpMinimize)
        service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)
        # objective function
        prob += lpSum( [ lpSum ([service[(i, j)]* ser_prov.iloc[i,j] for j in col_j ]) for i in row_i ] )
        # constrains - each service sum = total demand
        for i in row_i:
            prob += lpSum([service[(i,j)] for j in col_j]) == demand.iloc[i,0] , "" 
        prob += lpSum( [ lpSum([service[(i, j)]* w.iloc[j] for j in col_j ]) for i in row_i ] ) <= max_wage, "" 
                
        GLPK().solve(prob)
        # Solution summarize
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
        return dataset, tt

    return dataset, tt

def call_opt_ideal(w_weight, s_weight, wage, ser_prov, demand, ser_max, row_i, col_j, FTE_time):
    '''
    core LP to optimize the allocation by wage or priority
    '''
    prob = LpProblem("test1", LpMinimize)
    service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)
    # objective function
    prob += lpSum( [ lpSum([service[(i, j)]* (wage.iloc[j]*w_weight + ser_prov.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
    # constrains - each service sum = total demand
    for i in row_i:
        prob += lpSum([service[(i,j)] for j in col_j]) == demand.iloc[i,0] , "" 
    
    for i in row_i:
        for j in col_j:
            prob += service[(i,j)] >= 0
            prob += service[(i,j)] <= ser_max.iloc[i,j], ""
            
    # need zero
    GLPK().solve(prob)
    # Solution summarize
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
    return dataset, tt

def call_opt_current(w_weight, s_weight, wage, ser_prov, demand, ser_max, supply, row_i, col_j, FTE_time):
    '''
    core LP to optimize the allocation by wage or priority
    '''
    supply_check = ser_max.apply(sum, axis = 0)/FTE_time < supply
    if(   (~supply_check).all(axis = 1)[0]    ):
        prob = LpProblem("test1", LpMinimize)
        service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0, cat=pulp.LpInteger)
        # objective function
        prob += lpSum([lpSum([service[(i, j)]*(wage[j]*w_weight + sutability.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
        # constrains - each service sum = total demand
        for i in row_i:
            prob += lpSum([service[(i,j)] for j in col_j]) == total_demand.iloc[i,0], "" 
        # constrains - more than current supply
        for j in col_j:
            if( (supply[provider[j]] > 0)[0] ):
                prob += lpSum([service[(i,j)] for i in row_i]) >= supply[provider[j]]*FTE_time, "" 
                     
        GLPK().solve(prob)
        # Solution summarize
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
    else: 
        dataset = np.array(provider)[ supply_check.values[0]  ]
        print("Excess providers in " + ','.join(provider['provider_abbr'][0:3]))
        tt = 0
    return dataset, tt

def get_pattern(service_name, ser_prov, demand): 
    k = service_name['d_type']; 
    k1 = service_name['category']
    k2 = k + k1
    p = ser_prov.apply(lambda x: ''.join( ((x > 0)*1).astype('str') ), axis = 1)
    k2 = k2 + p
    df = pd.concat([k, k1, k2], axis = 1); df.columns = ['d_type','category','comb']
    k1 = df.groupby(["comb"]).size(); n_mem = len(k1) 

    # create assignment 
    ser_prov_mem = pd.DataFrame(index=range( len(ser_prov) ),columns=['mem'])
    for i in range( len(k1) ):
        ser_prov_mem.loc[ df['comb'] == k1.keys()[i] ] = i        
 
    # total Demand    
    demand_mem = pd.DataFrame(index=range(n_mem),columns=['demand'])
    for k1 in range(n_mem):
        g = demand.loc[ ser_prov_mem['mem'] == k1 , :].apply(sum, axis = 0)
        demand_mem.iloc[k1,:] = g
    return demand_mem

def assign_pattern( n_ser, provider, ser_prov_mem, total_demand, dataset):
    # assignback
    time_allocation = pd.DataFrame(index=range(n_ser),columns=provider)
    for k1 in range(n_mem):
        tmp =  ser_prov_mem['mem'] == k1; n = sum(tmp)
        if( sum(tmp) == 1 ):
            time_allocation.loc[np.where(tmp)[0][0],: ] = dataset.iloc[k1,:] 
        else: 
            i_demand = total_demand.loc[ np.where(tmp)[0],'total']; 
            i_demand = i_demand/sum(i_demand)
            p_demand = total_demand.loc[ np.where(tmp)[0],:].apply(sum, axis = 1)
            p_demand = p_demand/sum(p_demand)
            
            i = dataset.iloc[k1,:].apply( lambda x: x*i_demand )
            p = dataset.iloc[k1,:].apply( lambda x: x*i_demand )
            for j in range(n):
                time_allocation.loc[ np.where(tmp)[0][j], :] = i.iloc[:,j]
                #time_allocation.loc[ np.where(tmp)[0][j], 'Physician'] = p.iloc[1,j]
    return time_allocation
        
def call_assign_service(n_provider, n_mem, total_demand_mem):
    '''
    description
    '''
     
    # A and b
    x1 = np.repeat(1, n_provider); x2 = np.repeat(0, n_provider * (n_mem-1))
    A = np.concatenate((x1,x2), axis=0)
    for i in range(1, (n_mem-1)):
        x1 = np.repeat(0, n_provider*i)
        x2 = np.repeat(1, n_provider)
        x3 = np.repeat(0, n_provider * (n_mem-i-1))
        tmp = np.concatenate((x1,x2, x3), axis=0)
        A = np.vstack([A,tmp])
    x2 = np.repeat(1, n_provider); x1 = np.repeat(0, n_provider * (n_mem-1))
    tmp = np.concatenate((x1,x2), axis=0)
    A = np.vstack([A,tmp]); A = matrix(A.astype(float))
    b = total_demand_mem['total'].values.reshape((n_mem,1)); b = matrix(b.astype(float))

    G = -1.0 * np.identity(n_provider*n_mem); 
    G = matrix(G.astype(float))
    h = matrix( np.repeat(0, n_provider*n_mem) )

    # P and q
    x1 = np.repeat(1, 1); x2 = np.repeat(0, n_provider-1)
    tmp = np.concatenate((x1,x2), axis=0)
    M = np.tile(tmp, n_mem)
    for i in range(1, (n_provider-1)):
        x1 = np.repeat(0, i)
        x2 = np.repeat(1, 1)
        x3 = np.repeat(0, (n_provider-i-1))
        tmp = np.concatenate((x1,x2, x3), axis=0)
        A1 = np.tile(tmp, n_mem)
        M = np.vstack([M,A1])
    x2 = np.repeat(1, 1); x1 = np.repeat(0, n_provider-1)
    tmp = np.concatenate((x1,x2), axis=0)
    A1 = np.tile(tmp, n_mem)
    M = np.vstack([M,A1])
    P = dot(M.T, M); P = matrix(P.astype(float))
    sup = supply[provider].values.reshape((11,1))
    q = matrix(-2.0*dot(M.T, sup)); 
    sol = solvers.qp(P, q, G, h, A, b)
    d = np.array(sol['x']).reshape((n_mem,n_provider))
    dataset = round( pd.DataFrame(d) )
    dataset[ dataset < 1 ] = 0
    dataset.columns = provider
    #out = dataset.apply(sum, axis = 1)
    
    # assignback
    time_allocation = pd.DataFrame(index=range(n_ser),columns=provider)
    for k1 in range(n_mem):
        tmp =  ser_prov_mem['mem'] == k1; n = sum(tmp)
        if( sum(tmp) == 1 ):
            time_allocation.loc[np.where(tmp)[0][0],: ] = dataset.iloc[k1,:] 
        else: 
            i_demand = total_demand.loc[ np.where(tmp)[0],'total']; 
            i_demand = i_demand/sum(i_demand)
            p_demand = total_demand.loc[ np.where(tmp)[0],:].apply(sum, axis = 1)
            p_demand = p_demand/sum(p_demand)
            
            i = dataset.iloc[k1,:].apply( lambda x: x*i_demand )
            p = dataset.iloc[k1,:].apply( lambda x: x*i_demand )
            for j in range(n):
                time_allocation.loc[ np.where(tmp)[0][j], :] = i.iloc[:,j]
                #time_allocation.loc[ np.where(tmp)[0][j], 'Physician'] = p.iloc[1,j]
            


