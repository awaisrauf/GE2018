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
    # Results Data Frame
    list_results = []
    for constituency in constituencies:  
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
i = 0
for party in all_parties:
    if(i<6):
        party_to_number[party] = i                   
        i +=1
    else:
        party_to_number[party] = 6
               


constituencies = df_NA_list["Constituency"].unique()
constituencies = np.asarray(constituencies)
cordinates = pd.read_csv("data\\Election_2018_Stats\\NA_2018_centroids.csv")
real_result = pd.read_csv("results\\real_result.csv")
pred_result = pd.read_csv("results\\predicted_result.csv")
constituencies = real_result["Constituency"]



dic = {}
for constituency in constituencies:   
    constituency_cordinate_X = cordinates[cordinates["seat"] == constituency]["X"].tolist()[0]
    constituency_cordinate_Y = cordinates[cordinates["seat"] == constituency]["Y"].tolist()[0]
    original_party = real_result[real_result["Constituency"]==constituency]["Party"].tolist()[0]
    constituency_name = df_NA_list_2018[df_NA_list_2018["Constituency Number (ID)"]==constituency]["Constituency Name"].tolist()

    predicted_party = pred_result["Party"].tolist()[0]
    array = [constituency_cordinate_X,constituency_cordinate_Y,original_party,party_to_number[original_party],constituency, constituency_name]
    dic[constituency] = array
       

original_party = "Election Delyaed"      
dic["NA-60"]= [0,0,original_party,0,"NA-60","Rawalpinid"]

original_party = "Election Delyaed"      
dic["NA-103"]= [0,0,original_party,0,"NA-103","Faisalabad"]




with open( os.path.join("results","result.json"), "w") as write_file:
            json.dump(dic, write_file)