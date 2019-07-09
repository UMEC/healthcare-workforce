#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IBM Health Corp
"""
import pandas as pd
from pulp import *
import numpy as np
from numpy import dot
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt
import os

# Main function to run the three optimization functions
# geo: one of area shown in geo_are_list
# year: year that analysis is conducted
# current_year: current year. If current_year = year, then it will use current year demand/supply. 
# Otherwise, it will estimate demand and supply of the target year.
# option: one of three main function: 'ideal_staffing', 'ideal_staffing_current', 'service_allocation'
# sub_otion: for 'ideal_staffing' and 'ideal_staffing_current', users can further have "all_combination", "wage_max", "wage_weight"
# for service_allocation, subpotion = None
# sub_option_value: for wage_max = maximum wage, wage_weight = wage weight
# sut_target: ideal sutability target. Currently sutability indicates top & botton of the licence, and want to avoid top/botton of 
# the licence. Thus default target is 0.8. The function converts sutability score in a way that 0.8 has the smallest number (since we want to
# mininize the sutability score) If you think specific population segments need more skilled provider, then you can use
# higher sut_target. If it is quality score - and 1 is the 'best' quality, then target should be 1; and 0 is the best score then the 
# target should be 0
# collapse_group: this will be used for 'service_allocation'. If same types of providers can provide services belongs to the same
# encounter_category and service_category, one can collapse svc_desc and calculate service allocation. After time gets allocated,
# collapsed services will get corresponding service time proportionally. 
# FTE_time: 60x2080, used to convert FTE to min per year
# from pop_chronic_trend to overhead_work are input files

def readcsv(directory): 
    # read csv file in directory
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
    return dataframes
    

def main(geo, year, current_year, option, sub_option, sub_option_value, sut_target, collapse_group, FTE_time, 
         pop_chronic_trend, pop_chronic_prev, chron_care_freq, geo_area, service_characteristics, 
         pop_acute_need, population, provider_supply , pop_prev_need , provider_list , encounter_detail, overhead_work):
    pos_option = ('ideal_staffing', 'ideal_staffing_current', 'service_allocation')
    pos_sub_option = ("all_combination", "wage_max", "wage_weight", None)
    w_weight = None; s_weight = None; wage_max = None; 
    # this is the main function control the analysis - it gets csv files, then create input
    # then get optimization
    #===== you may need more through checking input checking
    if ( (option not in pos_option) | (sub_option not in pos_sub_option) ):
        #print("Invalid option. Option should be one of [all_combination, wage_max, wage_weight]. \
        #      \n Will calculate ideal staffing using wage weight = 1")
        w_weight = 1; s_weight = 0
        option = 'ideal_staffing' 
        pos_sub_option = "wage_weight"
        
    if (option == 'service_allocation'):
        #print("Service allocation have no subpotion. Using FTE minimization")
        sub_option = None
        
    if (sub_option == "all_combination") | (option == 'service_allocation'): 
        w_weight = None
        s_weight = None
        
    if (sub_option == "wage_max") : 
        w_weight = None 
        s_weight = None
        wage_max = int(sub_option_value)
        
    if ( sub_option == 'wage_weight' ):
        w_weight = float(sub_option_value)
        s_weight = float(1-w_weight)
        
    #print("Creating Input File.. It talkes few seconds")
    sdoh_score = geo_area.loc[geo_area['geo_area'] == geo,'sdoh_index']
    if( year != current_year):
        wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name = \
        input_create_future(geo, year, current_year, sut_target, sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need , population, provider_supply , pop_prev_need , 
             provider_list , encounter_detail, overhead_work )
        
    if( year == current_year):
        wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name = \
        input_create(geo, year, sut_target,  sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need , population, provider_supply , pop_prev_need , 
             provider_list , encounter_detail, overhead_work )
    
    #print("run optimization")
    s = resource_allocation(option, sub_option, wage, ser_prov, demand, supply, overhead_work, 
                   provider_list, service_name, collapse_group, w_weight, s_weight, wage_max, FTE_time)
    return s, supply


#=============================================================================
# two input creation functions - one for this year, the other for 
#============================================================================= 
def input_create(geo, year, sut_target, sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need, population, provider_supply, pop_prev_need , 
             provider_list , encounter_detail, overhead_work):
            
    # every provider should follow the order of provider_list['provider_abbr']
    population = population.loc[ population['pop_geo_area'] == geo, : ]
    population = population[ ['pop_sex','pop_age', year] ] 
    #total_pop = population[year].sum()

    # preventive demand
    prev_ser = encounter_detail.loc[ encounter_detail['encounter_category'] == 'Preventive',:]
    prev_df = pd.merge(prev_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])
    p_demand = []
    for i in range(len(prev_df)): # demand = rate_per_encounter * freq * n of population * time
        tmpid = prev_df.loc[i,'encounter_type']
        tmp = pop_prev_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
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
            t_demand = t_demand + r*freq.iloc[j]
        p_demand.append(t_demand) # frequency * population 
        
    f2f1 = prev_df['max_f2f_time']; f2f0 = prev_df['min_f2f_time']
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    prev_demand = prev_df['rate_per_encounter'] * f2f * p_demand
    prev_service_name  = prev_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    prev_ser_prv = prev_df[ provider_list['provider_abbr'] ]
    
    # acute demand
    acute_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Acute',:]
    acute_df = pd.merge(acute_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])

    a_demand = []
    for i in range(len(acute_df)): # demand = rate_per_encounter * prevalance * n of population * time
        tmpid = acute_df.loc[i,'encounter_type'] 
        tmp = pop_acute_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
        prev = tmp[ tmpid ].astype(float)
        s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
        s = s.loc[ tmp[tmpid] > 0 ]; e = e.loc[ tmp[tmpid] > 0 ]; g = g.loc[ tmp[tmpid] > 0 ]# total population need service
        prev = prev.loc[ tmp[tmpid] > 0 ];
        t_demand = 0
        for j in range( sum( tmp[tmpid] > 0 )): # won's have BOTH
            if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
            if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
            t_demand = t_demand + r *prev.iloc[j]/1000
        a_demand.append(t_demand) 
        # total demand
    f2f1 = acute_df['max_f2f_time']; f2f0 = acute_df['min_f2f_time']
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    
    acute_demand = acute_df['rate_per_encounter'] * f2f * a_demand
    acute_service_name  = acute_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    acute_ser_prv = acute_df[ provider_list['provider_abbr'] ]
    
    # chronic demand
    chro_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Chronic',:]
    chro_df = pd.merge(chro_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc']) 
    c_demand = []
    for i in range(len(chro_df)): # demand = rate_per_encounter * prev* freq * n of population * time
        tmpid = chro_df.loc[i,'encounter_type']
        freq = chron_care_freq.loc[ chron_care_freq[ tmpid ] > 0, ['chron_cond_abbr', tmpid]]
        t_demand = 0
        if( len(freq) > 0 ):
            if( len(freq) > 1 ):
                prev_freq = pop_chronic_prev[freq['chron_cond_abbr']].apply(lambda x: sum( (freq.iloc[:,1].values) * x.values ), axis = 1).astype(float)
                prev_freq = prev_freq.values
            else:
                prev_freq = pop_chronic_prev[ freq['chron_cond_abbr'] ]*freq.iloc[0,1].astype(float)
                prev_freq = prev_freq.values
                prev_freq = np.squeeze(prev_freq)

            tmp = pop_chronic_prev[ ['pop_min_age','pop_max_age','pop_sex' ] ]
            s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']

            for j in np.where(prev_freq > 0)[0]: 
                if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                  (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
                if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                  (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
                t_demand = t_demand + r *prev_freq[j]/1000
        
        c_demand.append(t_demand) 
    # total demand
    f2f1 = chro_df['max_f2f_time']; f2f0 = chro_df['min_f2f_time']
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    
    chronic_demand = chro_df['rate_per_encounter'] * f2f * c_demand
    chronic_service_name  = chro_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    chronic_ser_prv = chro_df[ provider_list['provider_abbr'] ]
            
    demand = pd.concat( [prev_demand, acute_demand, chronic_demand ] ).reset_index( drop=True )
    demand = demand.to_frame('demand') # demand
    ser_prov = pd.concat( [prev_ser_prv, acute_ser_prv, chronic_ser_prv ] ).reset_index( drop=True )
    service_name = pd.concat( [prev_service_name, acute_service_name, chronic_service_name] ).reset_index( drop=True )
    
    supply = provider_supply.loc[ provider_supply['provider_geo_area'] == geo, : ]
    supply = supply[  ['provider_abbr','provider_num','provider_mean_wage'] ] 
    supply.index = supply['provider_abbr']
    wage = supply['provider_mean_wage']/sum(supply['provider_mean_wage'])

    # sutability get optimized by sut_target
    if( sut_target > 0):
        for col in provider_list['provider_abbr']: 
            ser_prov[col] = ser_prov[col].replace('^\s*$', np.nan, regex=True).astype(float)
            v = 2*sut_target - ser_prov.loc[ser_prov[col] > sut_target, col] 
            ser_prov.loc[ ser_prov[col] > sut_target, col ] =  v 
            ser_prov[col] = 1- ser_prov[col]/sut_target
   
    # need to remove NA
    ser_prov = ser_prov.fillna(1.1) 
    # when licences not allow service, all will get 1.1, 1-top of the licence 0-super easy
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
    return wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name

def input_create_future(geo, year,current_year, sut_target, sdoh_score, pop_chronic_trend,  pop_chronic_prev, chron_care_freq, 
             geo_area, service_characteristics, pop_acute_need, population, provider_supply, pop_prev_need , 
             provider_list , encounter_detail, overhead_work):
    yeardiff = int(year) - int(current_year) 
    # every provider should follow the order of provider_list['provider_abbr']
    population = population.loc[ population['pop_geo_area'] == geo, : ]
    population = population[ ['pop_sex','pop_age', year] ] 
    #total_pop = population[year].sum()

    # preventive demand
    prev_ser = encounter_detail.loc[ encounter_detail['encounter_category'] == 'Preventive',:]
    prev_df = pd.merge(prev_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])
    p_demand = []
    for i in range(len(prev_df)): # demand = rate_per_encounter * freq * n of population * time
        tmpid = prev_df.loc[i,'encounter_type']
        tmp = pop_prev_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
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
            t_demand = t_demand + r*freq.iloc[j]
        p_demand.append(t_demand) # frequency * population 
    f2f1 = prev_df['max_f2f_time']; f2f0 = prev_df['min_f2f_time'] 
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    prev_demand = prev_df['rate_per_encounter'] * f2f * p_demand # rate_per_encounter
    prev_service_name  = prev_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    prev_ser_prv = prev_df[ provider_list['provider_abbr'] ]
    
    # acute demand == assume excel file updated
    acute_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Acute',:]
    acute_df = pd.merge(acute_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc'])

    a_demand = []
    for i in range(len(acute_df)): # demand = rate_per_encounter * prev * n of population * time
        tmpid = acute_df.loc[i,'encounter_type']
        
        tmp = pop_acute_need[ ['pop_min_age','pop_max_age','pop_sex',tmpid] ]
        prev = tmp[ tmpid ].astype(float)
        s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
        s = s.loc[ tmp[tmpid] > 0 ]; e = e.loc[ tmp[tmpid] > 0 ]; g = g.loc[ tmp[tmpid] > 0 ]# total population need service
        prev = prev.loc[ tmp[tmpid] > 0 ];
        t_demand = 0
        for j in range( sum( tmp[tmpid] > 0 )): # won's have BOTH
            if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
            if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
              (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
            t_demand = t_demand + r *prev.iloc[j]/1000 # proprtion per 1000
        a_demand.append(t_demand) 
        # total demand
    f2f1 = acute_df['max_f2f_time']; f2f0 = acute_df['min_f2f_time']
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    
    acute_demand = acute_df['rate_per_encounter'] * f2f * a_demand
    acute_service_name  = acute_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    acute_ser_prv = acute_df[ provider_list['provider_abbr'] ]
    
    # chronic demand
    chro_ser = encounter_detail.loc[encounter_detail['encounter_category'] == 'Chronic',:]
    chro_df = pd.merge(chro_ser, service_characteristics,  how='left', \
                      left_on=['svc_category','svc_desc'], right_on = ['svc_category','svc_desc']) 
    # service level
    c_demand = []
    for i in range(len(chro_df)): # demand = rate_per_encounter(prev)* freq * prev*n of population * time
        tmpid = chro_df.loc[i,'encounter_type']
        freq = chron_care_freq.loc[ chron_care_freq[ tmpid ] > 0, ['chron_cond_abbr', tmpid]]
        # disease level
        t_demand = 0; lf = len(freq)
        if( lf  > 0 ):
            for m in range(len(freq)):
                prev_freq = pop_chronic_prev[ freq.iloc[m, 0] ]*freq.iloc[m,1].astype(float)
                prev_freq = prev_freq.values
                prev_freq = np.squeeze(prev_freq)

                tmp1 = pop_chronic_trend[ freq.iloc[m, 0]]
                tmp = pop_chronic_prev[ ['pop_min_age','pop_max_age','pop_sex' ] ]
                s = tmp[ 'pop_min_age'].astype(int); e = tmp['pop_max_age'].astype(int); g = tmp['pop_sex']
                for j in np.where(prev_freq > 0)[0]: 
                    if(g.iloc[j]== 'F'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                      (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'F'), year ].sum()
                    if(g.iloc[j] == 'M'): r = population.loc[ (population['pop_age'] >= s.iloc[j]) & \
                      (population['pop_age'] <= e.iloc[j]) & (population['pop_sex'] == 'M'), year ].sum()
                    t_demand = t_demand + r * prev_freq[j]*(1+ tmp1[j])**(yeardiff)/1000
        c_demand.append(t_demand) # population * prev * freq
    # total demand
    f2f1 = chro_df['max_f2f_time']; f2f0 = chro_df['min_f2f_time']
    f2f = (f2f1 + f2f0)/5.0*sdoh_score.values
    
    chronic_demand = chro_df['rate_per_encounter'] * f2f * c_demand
    chronic_service_name  = chro_df[['encounter_category','encounter_type', 'svc_category', 'svc_desc']]
    chronic_ser_prv = chro_df[ provider_list['provider_abbr'] ]
            
    demand = pd.concat( [prev_demand, acute_demand, chronic_demand ] ).reset_index( drop=True )
    demand = demand.to_frame('demand') # demand
    ser_prov = pd.concat( [prev_ser_prv, acute_ser_prv, chronic_ser_prv ] ).reset_index( drop=True )
    service_name = pd.concat( [prev_service_name, acute_service_name, chronic_service_name] ).reset_index( drop=True )
    
    supply = provider_supply.loc[ provider_supply['provider_geo_area'] == geo, : ]
    nprovidernum = supply['provider_num']*(1+supply['provider_growth_trend'])**(yeardiff)
    nproviderwage = supply['provider_mean_wage']*(1+supply['provider_wage_trend'])**(yeardiff)
    supply = pd.concat([ supply['provider_abbr'], nprovidernum, nproviderwage], axis = 1)
    supply.columns = ['provider_abbr','provider_num','provider_mean_wage']
    supply.index = supply['provider_abbr']
    wage = supply['provider_mean_wage']/sum(supply['provider_mean_wage'])

    # sutability get optimized by sut_target
    if( sut_target > 0):
        for col in provider_list['provider_abbr']: 
            ser_prov[col] = ser_prov[col].replace('^\s*$', np.nan, regex=True).astype(float)
            v = 2*sut_target - ser_prov.loc[ser_prov[col] > sut_target, col] 
            ser_prov.loc[ ser_prov[col] > sut_target, col ] =  v 
            ser_prov[col] = 1- ser_prov[col]/sut_target
   
    # need to remove NA
    ser_prov = ser_prov.fillna(1.1) 
    # when licences not allow service, all will get 1.1, 1-top of the licence 0-super easy
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

    return wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name

#=============================================================================
# get input and find proper optimization function
#=============================================================================      
def resource_allocation(option, sub_option, wage, ser_prov, demand, supply, overhead_work,  provider_list, service_name, 
                        collapse_group, w_weight, s_weight, wage_max, FTE_time):
    # dimension   
    n_ser = len(demand)
    n_provider = len(provider_list)
    col_j = range(n_provider)
    row_i = range(n_ser)
    
    ser_max = pd.DataFrame(index=range(n_ser),columns=provider_list['provider_abbr'])
    for i in range( n_ser ):# service
        for m in provider_list['provider_abbr']:
            max_val  = (ser_prov.loc[i, m] <= 1) * demand.loc[i,'demand'] 
            
            ser_max.loc[i,m] = max_val 

    #====== optimization 
    total_wage = []; total_sutab = []; detail_result = []; 
    d = pd.DataFrame(index = provider_list['provider_abbr'])
    
    if( (option == 'ideal_staffing') | (option == 'ideal_staffing_current') ):
        if (sub_option == "all_combination" ):
            co = 0; s = {}
            for i in np.arange(0, 1.1, 0.1):
                wi_weight = i; si_weight = 1- i; co = co + 1
                if( option == 'ideal_staffing'):
                    dataset, tt = call_opt_ideal(wi_weight, si_weight, wage, ser_prov, demand, ser_max, row_i, col_j,FTE_time)
                if( option == 'ideal_staffing_current'):
                    dataset, tt = call_opt_current(wi_weight, si_weight, wage, ser_prov, demand, supply, ser_max, \
                                                   row_i, col_j,FTE_time, overhead_work, provider_list)
                # calculate statistics
                if tt == 0:
                    df = pd.DataFrame(np.nan, index=provider_list['provider_abbr'], columns = [i])
                    d = pd.concat( [ d, df], axis = 1)   
                    total_wage.append( np.nan )
                    total_sutab.append( np.nan )
                else:
                    dataset.columns = provider_list['provider_abbr'] # F2F
                    df = dataset.apply(sum, axis = 0)
                    doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
                    totaldoctime = overhead_work.loc[0, 'prop_f2f_tot']*demand.sum()[0]*doctime
                    cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
                    totalcortime = overhead_work.loc[1, 'prop_f2f_tot']*demand.sum()[0]*cortime
                    df = df + totaldoctime + totalcortime
                    df = (((df/FTE_time *10)/5).astype(float).round())/2
                    d = pd.concat( [d, df], axis = 1) 
                    total_wage.append( np.round( sum(df*supply['provider_mean_wage']), 0) )
                    total_sutab.append( sum((dataset * ser_prov).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)) )
                    dataset['weight'] = wi_weight
                    if(co == 1): detail_result =  pd.concat([service_name, dataset], axis = 1)
                    else: 
                        tmp =  pd.concat([service_name, dataset], axis = 1)
                        detail_result = pd.concat([detail_result, tmp], axis = 0)
            d.columns = ['w_0.0','w_0.1','w_0.2','w_0.3','w_0.4','w_0.5','w_0.6','w_0.7','w_0.8','w_0.9', 'w_1.0']
            s = {'total_wage': total_wage, 'total_sutab': total_sutab, 'FTE': d, 'detail_f2f_mini': detail_result}
        
        if( sub_option == "wage_weight"  ) :
            if( option == 'ideal_staffing'):
                dataset, tt = call_opt_ideal(w_weight, s_weight, wage, ser_prov, demand, ser_max,row_i, col_j,FTE_time)
            if( option == 'ideal_staffing_current'):
                dataset, tt = call_opt_current(w_weight, s_weight, wage, ser_prov, demand, supply, ser_max, \
                                               row_i, col_j,FTE_time,overhead_work, provider_list)
            # calculate statistics
            if tt == 0:
                s = 'Can not find optimal allocation. Check input'
            else:
                dataset.columns = provider_list['provider_abbr']
                detail_result = pd.concat([service_name, dataset], axis = 1)
                
                df = dataset.apply(sum, axis = 0)
                doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
                totaldoctime = overhead_work.loc[0, 'prop_f2f_tot']*demand.sum()[0]*doctime
                cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
                totalcortime = overhead_work.loc[1, 'prop_f2f_tot']*demand.sum()[0]*cortime
                df = df + totaldoctime + totalcortime
                df = (((df/FTE_time *10)/5).astype(float).round())/2
                df.columns = 'FTE'
                total_wage = np.round( sum(df*supply['provider_mean_wage']), 0) 
                total_sutab = np.round( sum((dataset * ser_prov).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)) ,2)
                # this is the code to get total wage and stability scores of individual provider types
                # if you think individual information is useful, please use similar code for 'all combination' option
                ind_wage = np.round( df*supply['provider_mean_wage'], 0) 
                ind_sutab = np.round( (dataset * ser_prov).apply(sum, axis = 0)/dataset.apply(sum, axis = 0) ,2)
                
                s = {}
                s = {'total_wage': total_wage, 'total_sutab': total_sutab, 'ind_wage': ind_wage,
                     'ind_sutab': ind_sutab, 'FTE': df, 'detail_f2f_mini': detail_result}
                
        if(sub_option ==  "wage_max"):
            s = call_opt_ideal_maxbudget(option, wage_max, wage, ser_prov, demand, supply, ser_max, row_i,\
                                         col_j, provider_list, overhead_work, FTE_time, service_name )
                             
    if( option == 'service_allocation' ):
        #================== get pattern 
        if(collapse_group == True):
            k = service_name['encounter_category']; 
            k1 = service_name['svc_category']
            k2 = k + k1
            p = ser_prov.apply(lambda x: ''.join( ((x <=1 )*1).astype('str') ), axis = 1)
            k2 = k2 + p
            df = pd.concat([k, k1, k2], axis = 1); df.columns = ['d_type','category','comb']
            k1 = df.groupby(["comb"]).size(); n_mem = len(k1)
            # create assignment 
            ser_prov_mem = pd.DataFrame(index=range( len(ser_prov) ),columns=['mem'])
            for i in range( n_mem ):
                ser_prov_mem.loc[ df['comb'] == k1.keys()[i] ] = i 
            # total Demand    
            demand_mem = pd.DataFrame(index=range(n_mem),columns=['demand'])
            for k1 in range(n_mem):
                g = demand.loc[ ser_prov_mem['mem'] == k1 , :].apply(sum, axis = 0)
                demand_mem.iloc[k1,:] = g
            ser_max_mem = pd.DataFrame(index=range(n_mem),columns=provider_list['provider_abbr'])
            for k1 in range(n_mem):
                max_val  = ser_max.loc[ ser_prov_mem['mem'] == k1, : ].apply(sum, axis = 0) 
                ser_max_mem.iloc[k1,:] = max_val
            dataset, current_demand = \
            call_assign_service(demand_mem, ser_max_mem, supply, overhead_work, provider_list, FTE_time)
            time_allocation = pd.DataFrame(index=range(n_ser),columns=provider_list['provider_abbr'])
            #k1 = df.groupby(["comb"]).size()
            for k1 in range(n_mem):
                tmp =  ser_prov_mem['mem'] == k1; n = sum(tmp)
                if( sum(tmp) == 1 ):
                    time_allocation.loc[np.where(tmp)[0][0],: ] = dataset.iloc[k1,:] 
                else: 
                    i_demand = demand.loc[ np.where(tmp)[0],'demand']; 
                    i_demand = i_demand/sum(i_demand)
                    i = dataset.iloc[k1,:].apply( lambda x: x*i_demand )
                    for j in range(n):
                        time_allocation.loc[ np.where(tmp)[0][j], :] = i.iloc[:,j]  
            dataset = time_allocation
            dataset = pd.concat([service_name, dataset], axis = 1)
        else: # not collapsing
            dataset, current_demand = \
            call_assign_service(demand, ser_max, supply, overhead_work, provider_list, FTE_time)
            dataset = pd.concat([service_name, dataset], axis = 1)
            
        s = {}
        s = {'FTE': current_demand,  'detail_f2f_mini': dataset}

    return s

#=============================================================================
# ideal_staffing or ideal_staffing_current when maximum budget is given
#=============================================================================
   
def call_opt_ideal_maxbudget(option, wage_max, wage, ser_prov, demand, supply, ser_max, row_i, col_j, provider_list, 
                             overhead_work, FTE_time , service_name):
    '''
    core LP to optimize the allocation by wage or priority --- find something that using grid search
    '''
    total_wage = []; total_sutab = []; detail_result=[]; 
    v = np.arange(0, 1.01, 0.1); w_weight = None; s= None
    for i in v:
        wi_weight = i; si_weight = 1- i; 
        if( option == 'ideal_staffing'):
            dataset, tt = call_opt_ideal(wi_weight, si_weight, wage, ser_prov, demand, ser_max, row_i, col_j,FTE_time)
        if( option == 'ideal_staffing_current'):
            dataset, tt = call_opt_current(wi_weight, si_weight, wage, ser_prov, demand, supply, ser_max, row_i, col_j,\
                                           FTE_time, overhead_work, provider_list)
        if tt > 0:
            # calculate statistics
            dataset.columns = provider_list['provider_abbr']
            df = dataset.apply(sum, axis = 0)
            doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
            totaldoctime = overhead_work.loc[0, 'prop_f2f_tot']*demand.sum()[0]*doctime
            cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
            totalcortime = overhead_work.loc[1, 'prop_f2f_tot']*demand.sum()[0]*cortime
            df = df + totaldoctime + totalcortime
            df = (((df/FTE_time *10)/5).astype(float).round())/2
            total_wage.append( np.round( sum(df*supply['provider_mean_wage']), 0) )
        else: 
            s = 'Excess supply'
    
    if(s == None): 
        if( wage_max < min(total_wage) ):
            s = 'Try higher maximum wage. Available minimum/maximum wage to minimize wage or minimize \
            sutability score is:' +min(total_wage).round().astype(str)+ ' and '+  max(total_wage).round().astype(str)
    else: wage_max = 0
    
    if( wage_max >= min(total_wage) ):
        #print( 'Narrow the search.. it takes few seconds')
        mini = min( np.where( np.array(total_wage) < wage_max )[0] )
        if mini == 0: w_weight = 0
        else:
            total_wage = []; sv = np.arange(v[mini]-0.1, v[mini]+0.001, 0.01)
            for i in sv:
                wi_weight = i; si_weight = 1- i; 
                if( option == 'ideal_staffing'):
                    dataset, tt = call_opt_ideal(wi_weight, si_weight, wage, ser_prov, demand, ser_max, row_i, col_j,FTE_time)
                if( option == 'ideal_staffing_current'):
                    dataset, tt = call_opt_current(wi_weight, si_weight, wage, ser_prov, demand, supply, ser_max, row_i, \
                                                   col_j,FTE_time, overhead_work, provider_list)
                if tt > 0:
                    # calculate statistics
                    dataset.columns = provider_list['provider_abbr']
                    df = dataset.apply(sum, axis = 0)
                    doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
                    totaldoctime = overhead_work.loc[0, 'prop_f2f_tot']*demand.sum()[0]*doctime
                    cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
                    totalcortime = overhead_work.loc[1, 'prop_f2f_tot']*demand.sum()[0]*cortime
                    df = df + totaldoctime + totalcortime
                    df = (((df/FTE_time *10)/5).astype(float).round())/2
                    total_wage.append( np.round( sum(df*supply['provider_mean_wage']), 0) )
                else: 
                    total_wage.append(0 )
            mini = min( np.where( np.array(total_wage) < wage_max )[0] )
            w_weight = sv[mini]
    
        s_weight = 1-w_weight
        if( option == 'ideal_staffing'):
            dataset, tt = call_opt_ideal(w_weight, s_weight, wage, ser_prov, demand, ser_max,row_i, col_j,FTE_time)
        if( option == 'ideal_staffing_current'):
            dataset, tt = call_opt_current(w_weight, s_weight, wage, ser_prov, demand, supply, ser_max,  row_i, col_j,\
                                           FTE_time, overhead_work, provider_list)
        
        # calculate statistics
        if tt == 0:
            s = 'Can not find optimal allocation. Change input'
        else:
            dataset.columns = provider_list['provider_abbr']
            detail_result = pd.concat([service_name, dataset], axis = 1)
            df = dataset.apply(sum, axis = 0)
            doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
            totaldoctime = overhead_work.loc[0, 'prop_f2f_tot']*demand.sum()[0]*doctime
            cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
            totalcortime = overhead_work.loc[1, 'prop_f2f_tot']*demand.sum()[0]*cortime
            df = df + totaldoctime + totalcortime
            df = (((df/FTE_time *10)/5).astype(float).round())/2
            df.columns = 'FTE'
            total_wage = np.round( sum(df*supply['provider_mean_wage']), 0) 
            total_sutab = np.round( sum((dataset * ser_prov).apply(sum, axis = 0))/sum(dataset.apply(sum, axis = 0)), 2)
            ind_wage = np.round( df*supply['provider_mean_wage'], 0) 
            ind_sutab = np.round( (dataset * ser_prov).apply(sum, axis = 0)/dataset.apply(sum, axis = 0) ,2)
            #tmp =  pd.concat([service_name, dataset], axis = 1)
            s = {}
            s = {'total_wage': total_wage, 'total_sutab': total_sutab, 'ind_wage': ind_wage,
                     'ind_sutab': ind_sutab, 'FTE': df, 'detail_f2f_mini': detail_result}
    return s

#=============================================================================
# service allocation - quadratic programming 
#=============================================================================           
def call_assign_service(demand_mem, ser_max_mem, supply, overhead_work, provider_list, FTE_time):
    # overhead time first
    n_mem = len(demand_mem); n_provider = len(supply); tF2F = sum(demand_mem['demand'])
    doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
    overheadtime = overhead_work.loc[0, 'prop_f2f_tot']*tF2F*doctime
    cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
    overheadtime  = overheadtime  + overhead_work.loc[1, 'prop_f2f_tot']*tF2F*cortime 
    
    # total demand 
    s = supply['provider_num']*FTE_time
    if( all(s-overheadtime >0) ):  s = s-overheadtime # if overhead is bigger than current supply then
    # find optimal only based on F2F. Otherwise, find minimum variance between supply and F2F + overhead
        
    # P and q - object function
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
    M = np.vstack([M,A1]) # n_mem x n_provider
    P = 0.5*dot(M.T, M); P = matrix(P.astype(float)) # n_provider x n_provider
    sup = s.values.reshape((n_provider,1)) # n_provider x 1
    q = matrix( (-1.0*dot(M.T, sup)).astype(float) ); 
    
    # G and h minimum values. some are zero and some has maximum. Only has maximum
    g1 = -1.0 * np.identity(n_provider*n_mem); 
    g2 = 1.0 * np.identity(n_provider*n_mem); 
    h1 = np.repeat(0, n_provider*n_mem)
    h2 = ser_max_mem.values.reshape(1,n_provider*n_mem).astype(float); h2=h2[0]
    h3 = h2==0; 
    g02 = g2[h3,:]
    h02 = h2[h3]
    h3 = h2 != 0; 
    g11 = g1[h3,:]; g12 = g2[h3,:]
    h11 = h1[h3]; h12 = h2[h3]
    G = np.concatenate((g11,g12), axis=0)
    G = matrix(G.astype(float))
    h = np.concatenate((h11,h12), axis=0).astype(float)
    h = matrix(h)
    
    # A and b (sum of service = demand)   and some zeros             
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
    A = np.vstack([A,tmp,g02]); 
    A = matrix(A.astype(float))
    b = demand_mem['demand'].values #.reshape((n_mem,1)); 
    b = np.concatenate((b,h02), axis=0)
    b = matrix(b.astype(float))

    solvers.options['show_progress'] =  False
    sol = solvers.qp(P, q, G, h, A, b)
    d = np.array(sol['x']).reshape((n_mem,n_provider))
    dataset = pd.DataFrame(d)
    dataset[ dataset < 0.0001 ] = 0
    dataset.columns = supply['provider_abbr']

    df = dataset.apply(sum, axis = 0)
    df = df + overheadtime 
    df = (((df/FTE_time *10)/5).astype(float).round())/2
   
    current_demand = df
    return dataset, current_demand

#=============================================================================
# linear programming used for ideal staffing
#=============================================================================
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
    GLPK(msg=0).solve(prob)

    # Solution summarize
    dataset = pd.DataFrame(np.nan, row_i, col_j); 
    tt = 0 
    for v in prob.variables():
        m = v.name 
        m =  m.replace( 'service_(' , "")
        m =  m.replace( '_' , "")
        m =  m.replace( ')' , "")
        m = m.split(',')
        dataset.iloc[ int(m[0]), int(m[1]) ] = v.varValue
        tt = tt + v.varValue
          
    return dataset, tt

#=============================================================================
# linear programing used for ideal staffing constrined by current supply
#=============================================================================
def call_opt_current(w_weight, s_weight, wage, ser_prov, demand, supply, ser_max, row_i, col_j, FTE_time, \
                     overhead_work, provider_list):
    '''
    core LP to optimize the allocation by wage or priority
    '''
    tF2F = sum(demand['demand'])
    doctime = overhead_work.loc[0, provider_list['provider_abbr']  ]
    overheadtime = overhead_work.loc[0, 'prop_f2f_tot']*tF2F*doctime
    cortime = overhead_work.loc[1, provider_list['provider_abbr']  ]
    overheadtime  = overheadtime  + overhead_work.loc[1, 'prop_f2f_tot']*tF2F*cortime 
    totaldemand = ser_max.apply(sum, axis = 0) + overheadtime
   
    current_supply = supply['provider_num']
    supply_check = totaldemand  > current_supply*FTE_time # more demand than supply
    if(   sum(supply_check) == len(current_supply)   ): # there is no surplus of supply
        f2f_supply = current_supply*FTE_time - overheadtime
        f2f_supply.loc[ f2f_supply < 0 ] = 0 
        prob = LpProblem("test1", LpMinimize)
        service = LpVariable.dicts("service", ((i, j) for i in row_i for j in col_j ), lowBound = 0)
        # objective function
        prob += lpSum([lpSum([service[(i, j)]*(wage.iloc[j]*w_weight + ser_prov.iloc[i,j]*s_weight) for j in col_j ]) for i in row_i ] )
        # constrains - each service sum = total demand
        for i in row_i:
            prob += lpSum([service[(i,j)] for j in col_j]) == demand.iloc[i,0], "" 
        # constrains - more than current supply
        for j in col_j:
            prob += lpSum([service[(i,j)] for i in row_i]) >= f2f_supply.iloc[j], "" 
        # maximum - no licence zero; otherwise can take total demand       
        for i in row_i:
            for j in col_j:
                prob += service[(i,j)] >= 0
                prob += service[(i,j)] <= ser_max.iloc[i,j], ""
                     
        GLPK(msg = 0).solve(prob)
        # Solution summarize
        dataset = pd.DataFrame(np.nan, row_i, col_j); 
        tt = 0 
        for v in prob.variables():
            m = v.name 
            m =  m.replace( 'service_(' , "")
            m =  m.replace( '_' , "")
            m =  m.replace( ')' , "")
            m = m.split(',')
            dataset.iloc[ int(m[0]), int(m[1]) ] = v.varValue
            tt = tt + v.varValue     
        if tt==0: 
            print( "Excess providers. Try reduced number of providers" )
            dataset = np.nan
    else: 
        print( 'Excess providers in ' + ','.join( current_supply[ ~supply_check ].index ) )
        tt = 0
        dataset = np.nan
    return dataset, tt
#=============================================================================
# from here all are utility functions such as summarize output or plot figures using output from 'main'
#=============================================================================
def summaryout(out, sub_option):
    df = None
    # put outputs from main function - total wage, total sutability and FTE - side by side
    if( isinstance(out, dict) ):
        if( sub_option == 'all_combination'):
            df1 = pd.DataFrame({'Total Wage': out['total_wage']}, index = out['FTE'].columns)
            df2 = pd.DataFrame({'Total sutability': out['total_sutab']}, index = out['FTE'].columns)
            df3 = out['FTE'].T
            df = pd.concat([df1,df2, df3], axis = 1)
        if( (sub_option == 'wage_weight') | (sub_option == 'wage_max')  ):
            d1 = []; d1.append(out['total_wage'])
            d2 = []; d2.append(out['total_sutab'])
            df1 = pd.DataFrame({'Total Wage': d1})  #, index = out1['FTE'].columns)
            df2 = pd.DataFrame({'Total sutability': d2}) #, index = out1['FTE'].columns)
            df3 = pd.DataFrame( out['FTE'].values.reshape(1,len(out['FTE'])), columns=out['FTE'].index)
            df = pd.concat([df1,df2, df3], axis = 1)
    else: df = out
    return df
  
#added figsize & savefig
def plotall(thisweight, s, supply, option, sub_option, provider_list):
    # plot the output from main functions
    current_supply =  supply['provider_num']
    if( isinstance(s, dict) ):
        if( ((option =='ideal_staffing') | (option == 'ideal_staffing_current')) & \
           (sub_option == "all_combination")  ):
            # need input from user
            getthis = np.where( np.round(np.arange(0, 1.1, 0.1),1) == thisweight)[0]
            tmp = s['detail_f2f_mini']
            tmp = tmp.loc[ np.round(tmp['weight'],1) == thisweight, :]
            plot_wage_sutability(s['total_wage'], s['total_sutab'])
            plot_provider_by_service(tmp , provider_list['provider_abbr'])
            plot_service_by_provider(tmp , provider_list['provider_abbr'])
            plot_supply_demand(s['FTE'].iloc[:,getthis], current_supply)
            
        if( (sub_option == "wage_weight" ) | (sub_option == "wage_max" ) | (option =='service_allocation') ):
            tmp = s['detail_f2f_mini']
            plot_provider_by_service(tmp , provider_list['provider_abbr'])
            plot_service_by_provider(tmp , provider_list['provider_abbr'])
            plot_supply_demand(s['FTE'], current_supply)

def plot_wage_sutability(total_wage, total_sutab):
    fig, ax1 = plt.subplots(figsize = (12, 6))
    #fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Weight of Wage (or 1-Weight of Priority)')
    ax1.set_ylabel('Total Wage (unit = 1000$)', color=color)
    t = np.arange(0, 1.1, 0.1)
    total_wage1 = [x /1000 for x in total_wage]
    ax1.plot(t, total_wage1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Mean Sutability Score', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, total_sutab, color=color)
    ax2.tick_params(axis='y', labelcolor=color)             
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    #fig.savefig('path/wage_suit.png');plt.close(fig)   


def plot_supply_demand(current_demand, current_supply):
    p = pd.concat([current_demand, current_supply], axis = 1)
    p.columns = ['current_needs','current_supply']
    p.plot(kind='bar', figsize = (12, 6)) # supply demand plot
    #p.plot(kind='bar')
    plt.title('Needs vs. Supply')
    fig = plt.gcf() #get reference to current figure
    plt.show()
    #fig.savefig('path/need_supply.png');plt.close(fig)
    
    
def plot_provider_by_service(detail_result, providerlist):    
    p = detail_result.groupby('svc_category')[providerlist].sum()
    fig, ax = plt.subplots(figsize = (12, 6))
    #fig, ax = plt.subplots()
    p.T.plot(kind='bar',stacked=True, ax=ax, width=0.4)
    lgd = ax.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    #ax.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    plt.title('F2F Service allocation by provider type (Min)')
    plt.show()
    #fig.savefig('path/provider_service.png', bbox_extra_artists=(lgd,), bbox_inches='tight');plt.close(fig)


def plot_service_by_provider(detail_result, providerlist):
    p = detail_result.groupby('svc_category')[providerlist].sum()
    fig, ax = plt.subplots(figsize = (12, 6))
    #fig, ax = plt.subplots()
    p.plot(kind='bar',stacked=True, ax=ax, width=0.4)
    lgd = ax.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    #ax.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    plt.title('F2F Service allocation by service type (Min)')
    plt.show()
    #fig.savefig('path/service_provider.png', bbox_extra_artists=(lgd,), bbox_inches='tight');plt.close(fig)




