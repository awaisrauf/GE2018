# -*- coding: utf-8 -*-
"""
@descrption: Compares predicted results with the origianl reults
@author: Awais
"""
import pandas as pd
import json
import os
import numpy as np
import time
from preprocessing import Vote_distribution_preprocessed,Result_2018,NA_list_preprocessed
from la import l2_Exact, l1_LP
from model import final_model


df_NA_list_2018 = NA_list_preprocessed()
#==============================================================================
#  processes on real results taken from Pakistan's Election Commission           
#==============================================================================
def real_results():
    df_NA_list = Result_2018()
    constituencies = df_NA_list.seat.unique().tolist()
    # Results Data Frame
    list_results = []
    for constituency in constituencies:  
        print([constituency])
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["seat"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
       
            
        candidate_prob = current_constituency_data["results__votes"].tolist()
        list_candidates = current_constituency_data["results__candidate"].tolist()
        list_parties = current_constituency_data["results__party"].tolist()
        winning_candidate_name = list_candidates[np.argmax(candidate_prob)]
        winning_party_name = list_parties[np.argmax(candidate_prob)]
        list_results.append([constituency, winning_candidate_name,winning_party_name])

       
    df_results=pd.DataFrame(list_results,columns=['Constituency',
    'Winning Candidate', "Party"])
        
    # save results to csv
    df_results.to_csv("results/real_result.csv",index=False) 

   
#==============================================================================
#  Finds accuraccy            
#==============================================================================
def accuracy_seat_wise(pred_result=None):
    
    real_result = pd.read_csv("data\\results\\real_result.csv")
    if pred_result is None:
        pred_result = pd.read_csv("data\\results\\result_party.csv") 
    else:
        pred_result = pred_result
    constituencies =  real_result["Constituency"].unique().tolist()
    score = 0
    non_score = 0
    wrong_score = 0
    for constituency in constituencies:
       try:
           pred_party = pred_result[pred_result["Constituency"] == constituency]["Party"].tolist()[0]
           real_party = real_result[real_result["Constituency"] == constituency]["Party"].tolist()[0]
           if( real_party==pred_party ):
               score +=1 
           else:
               wrong_score +=1
       except:
           print(constituency)
           non_score +=1
    print(wrong_score)    
       
    return score
	
	
# =============================================================================
# find accuracy party share wise
# =============================================================================
def accuracy_share_wise(pred_result):
    real_result = pd.read_csv("data\\results\\real_result.csv")
    real_result_party_wise = real_result["Party"].value_counts()
    parties = ["PTI","PML-N","PPPP","MMA"]
    error,pred_total,real_total  = 0,0,0
    for party in parties:
        error = error+ abs(real_result_party_wise[party]- pred_result[party])
        pred_total += real_result_party_wise[party]
        real_total += pred_result[party]
    error += abs(pred_total-real_total)
    return 270-error
	
	
# =============================================================================
# Finds votes difference between predicted and actual       
# =============================================================================
def results_province():
    real_result = pd.read_csv("data\Election_2018_Stats\Election_result_2018.csv")
    pred_result = pd.read_csv()
	
	
	
# =============================================================================
# Compare different methods
# =============================================================================
def compare_methods(method):
    # l1 norm: Bayesian optimization
    print("Starting..")
    start_time = time.time()
    if  method == "L1-BO":
        paras = parameter_serach(iters=15,norm="l1")
    elif method == "L1-LP":
        paras = l1_LP()
    elif method == "L2-EX":
        paras = l2_Exact()
    elif method == "L2-BO":
        paras = parameter_serach(iters=15,norm="l1")
        
    party_wise_result, seat_wise_result = final_model(paras[:12])
    end_time = time.time()
    print(end_time)
    time_taken = end_time-start_time
    acc_share = accuracy_share_wise(party_wise_result)
    acc_seat = accuracy_seat_wise(seat_wise_result)
    
    result = [method,acc_seat,acc_share,time_taken]
    return result	
    