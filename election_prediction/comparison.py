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
i = 5
other = 11
for party in all_parties:
    if(i<11):
        party_to_number[party] = i                   
        i +=1
    else:
        party_to_number[party] = other
party_to_number["PKMAP"] = other
party_to_number["Ch.Nissar"] = other
party_to_number["TLP"] = other
party_to_number["GDA"] = other
party_to_number["Barabri Party Pakistan"] = other 
party_to_number["PSP"] = other 
party_to_number["Amun Taraqqi Party"] = other 
party_to_number["Pakistan Rah-e-Haq Pak"] = other 

               

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
        orignial_label = original_party+":"+":"+constituency+":"+constituency_name[0]
    except:
        orignial_label = original_party+":"+":"+constituency
    try:
        constituency_name = constituency_name[0]
    except:
        constituency_name = "" 
    # to avoid having [] inspite of partyy    
    if(pred_result[pred_result["Constituency"]==constituency]["Party"].tolist()):
        predicted_party = pred_result[pred_result["Constituency"]==constituency]["Party"].tolist()[0]
        predicted_label = predicted_party+":"+":"+constituency+":"+constituency_name
    else:
        predicted_party = "PML-N"
        predicted_label = predicted_party+":"+":"+constituency+":"+constituency_name
    #print(constituency,predicted_party)
    array_real = [constituency_cordinate_X,constituency_cordinate_Y,orignial_label,party_to_number[original_party]]
    if(predicted_party in all_parties):
        array_pred = [constituency_cordinate_X,constituency_cordinate_Y,predicted_label,party_to_number[predicted_party]]
    else:
        array_pred = [constituency_cordinate_X,constituency_cordinate_Y,predicted_label,other]

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
    pred_result = pd.read_csv("results\\result_party.csv")   
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
       
    return score,non_score       