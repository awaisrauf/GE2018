# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:34:56 2018

@author: ss
"""
import pandas as pd
import json
import os
import numpy as np
from preprocessing import Vote_distribution_preprocessed,Result_2018,NA_list_preprocessed

df_NA_list_2018 = NA_list_preprocessed()


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


df_NA_list = pd.read_csv("results/real_result.csv") 
all_parties = df_NA_list["Party"].value_counts().index.tolist()
party_to_number = {}
i = 50
for party in all_parties:
    if(i<56):
        party_to_number[party] = i                   
        i +=1
    else:
        party_to_number[party] = 57
party_to_number["PKMAP"] = 57
party_to_number["Ch.Nissar"] = 57 
party_to_number["TLP"] = 57
party_to_number["GDA"] = 57 
party_to_number["Barabri Party Pakistan"] = 57 
party_to_number["PSP"] = 57 
party_to_number["Amun Taraqqi Party"] = 57 
party_to_number["Pakistan Rah-e-Haq Pak"] = 57 

               

real_results()
constituencies = df_NA_list["Constituency"].unique()
constituencies = np.asarray(constituencies)
cordinates = pd.read_csv("data\\Election_2018_Stats\\NA_2018_centroids.csv")
real_result = pd.read_csv("results\\real_result.csv")
pred_result = pd.read_csv("results\\result_party.csv")
constituencies_real = real_result["Constituency"]
constituencies_pred = pred_result["Constituency"]




dic_predicted = {}
dic_real = {}
for constituency in constituencies_real:   
    constituency_cordinate_X = cordinates[cordinates["seat"] == constituency]["X"].tolist()[0]
    constituency_cordinate_Y = cordinates[cordinates["seat"] == constituency]["Y"].tolist()[0]
    original_party = real_result[real_result["Constituency"]==constituency]["Party"].tolist()[0]
    constituency_name = df_NA_list_2018[df_NA_list_2018["Constituency Number (ID)"]==constituency]["Constituency Name"].tolist()
    try:
        constituency_name = constituency_name[0]
    except:
        constituency_name = "Unknown" 
    # to avoid having [] inspite of partyy    
    if(pred_result[pred_result["Constituency"]==constituency]["Party"].tolist()):
        predicted_party = pred_result[pred_result["Constituency"]==constituency]["Party"].tolist()[0]
    else:
        predicted_party = "PML-N"
    print(constituency,predicted_party)
    array_real = [constituency_cordinate_X,constituency_cordinate_Y,original_party,party_to_number[original_party],constituency, constituency_name]
    if(predicted_party in all_parties):
        array_pred = [constituency_cordinate_X,constituency_cordinate_Y,predicted_party,party_to_number[predicted_party],constituency, constituency_name]
    else:
        array_pred = [constituency_cordinate_X,constituency_cordinate_Y,predicted_party,6,constituency, constituency_name]

    dic_real[constituency] = array_real
    dic_predicted[constituency] = array_pred
    

original_party = "Election Delyaed"      
dic_real["NA-60"]= [0,0,original_party,0,"NA-60","Rawalpinid"]
dic_predicted["NA-60"]= [0,0,original_party,0,"NA-60","Rawalpinid"]

original_party = "Election Delyaed"      
dic_real["NA-103"]= [0,0,original_party,0,"NA-103","Faisalabad"]
dic_predicted["NA-103"]= [0,0,original_party,0,"NA-103","Faisalabad"]




with open( os.path.join("results","result_real.json"), "w") as write_file:
            json.dump(dic_real, write_file)

with open( os.path.join("results","result_predicted.json"), "w") as write_file:
            json.dump(dic_predicted, write_file)         
#==============================================================================
#  Finds accuraccy            
#==============================================================================
def accuracy():
    real_result = pd.read_csv("results\\real_result.csv")
    pred_result = pd.read_csv("results\\dunya_result_party.csv")   
    constituencies =  real_result["Constituency"].unique().tolist()
    score = 0
    non_score = 0
    for constituency in constituencies:
       try:
           pred_party = pred_result[pred_result["Constituency"] == constituency]["Party"].tolist()[0]
           real_party = real_result[real_result["Constituency"] == constituency]["Party"].tolist()[0]
           if( real_party==pred_party ):
               score +=1   
       except:
           print(constituency)
           non_score +=1
       
       
    return score,non_score       