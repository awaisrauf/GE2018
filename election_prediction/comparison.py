# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:34:56 2018

@author: ss
"""
import pandas as pd
import json
import os
import numpy as np
from preprocessing import Vote_distribution_preprocessed

def Result_2018():
    df_result_2018 = pd.read_csv("E:\Semester3\GE2018\GE2018\election_prediction\data\Election_2018_Stats\Election_result_2018.csv")
    # fill na values with values above
    df_result_2018 = df_result_2018.fillna(method="ffill")
    
    replacements = {
          # standredize Independent name in data      
          'Independent': 'IND',
          'Independent Candidate': 'IND',
          ' Independent': 'IND',
          'Indepdendent': 'IND',
          # standredize PTI name in data
          'Pakistan Tehreek-e-lnsaf':'PTI',
          'Pakistan Tehreek e Insaf': 'PTI',
          'Pakistan Tehreek E Insaf': 'PTI',
          'Pakistan Tehreek e Insaaf': 'PTI',
          'Pakistan tehreek-e-Insaf': 'PTI',
          'Pakistan Tehreek e insaf': 'PTI',
          'PakistanTehreek-e-Insaf':  'PTI',
          'Pakisyan Tehreek e Insaaf': 'PTI',
          'Pakistan Tehreek-e-lnsaf': 'PTI',
          'Pakistan tehreek e Insaf': 'PTI',
          'Pakistan Tehreek-e-Insaf': 'PTI', 
          'Pakistan Tahreek-e-Insafa': 'PTI',
          'Tehrik e Insaf': 'PTI',
          # standredize PML-N name in data
          'Pakistan Muslim League (N)': 'PML-N',
          'Pakistan Muslim League(N)': 'PML-N', 
          'Pakistan Muslim League\n(N)': 'PML-N',                    
          'PMLN': 'PML-N',
          'PMLN': 'PML-N',
          'PML (N)': 'PML-N',
          'PML -N': 'PML-N',   
          'Pakistan Muslim League(N)' : 'PML-N', 
          # standredize PPPP name in data                       
          'Pakistan Peoples Party Parliamentarians': 'PPPP',
          'Pakistan Peoples party parlimentarians':'PPPP',
          'Pakistan Peoples party parlimentarians': 'PPPP',
          'Pakistan Peoples Party Parlimentarians': 'PPPP',
          'Pakistan Peoples Party\nParliamentarians': 'PPPP',
          'Pakistan Peoples Party': 'PPPP',
          'Pakistan Peoples Part Parliamentarians': 'PPPP',
          'Pakistan peopkes party parlimentarians': 'PPPP',
          'Pakistan People Party Parlianmentray': 'PPPP',
          # 
          'MUTAHIDA MAJLIS AMAL PAKISTAN': 'MMA',
          'Mutahida Majlas-e-Amal Pakistan':'MMA',
          'MUTAHIDA MAJLIS AMAL PAKISTAN ': 'MMA',
          'Mutthida Majlis-E-Amal Pakistan': 'MMA',
          'Mutthida Majlis-e-Amal Pakistan': 'MMA',
          'Mutahida Majlas-e-Amal Pakistan': 'MMA',
          'MUTTHIDA MAJLIS-E-AMAL PAKISTAN': 'MMA',
          'MUTTAHIDA MAJLIS-E- AMAL PAKISTAN': 'MMA',
          'Muthida Majlis e Amal Pakistan': 'MMA',
          'Mutihida Majlis e Amal Pakistan': 'MMA',
          'M.M.A' : 'MMA',
          'Muttahida Majlis-e-Amal Pakistan':'MMA',
          #
          'Mutahida Qaumi Movemebt Pakistan': 'MQM',
          'Muttahida Qaumi Movement Pakistan': 'MQM',
          # 
          'Tehreek Labbaik Pakistan': 'TLP',
          'Tehreek labbaik Pakistan': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tahreek Labbaik pakistan': 'TLP',
          'Tehreek e Labbaik Pakistan': 'TLP',
          'Tehrek e labbaik Pakistan' : 'TLP',
          'Tehrik e Labbaik Pakistan': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tehreek e labbaik Pakistan':'TLP',
          'Tehreek-e-Labbaik Pakistan': 'TLP',
          'Tehreek e Labbaik Pakistan TLI ': 'TLP',
          #
          'Awami National Party': 'ANP',
          'Avvami National Party': 'ANP',
          #
          'Pak Sarzameen Party': 'PSP',
          'Pak SarZamen Party': 'PSP',
          #
          'Pakistan Muslim League': 'PML-Q',
          'PML -Q':'PML-Q',
          #
          'Balochistan National Party': 'BNP',
          'Balochistan National Party': 'BNP',
          #
          'Balochistan Awami Party': 'BAP',
          'Balochistan Awami Party': 'BAP',
          #
          'Pashtoonkhwa Milli Awami Party': 'PKMAP',
          'PashtoonKhwa Milli Awami party': 'PKMAP',
          'Pakhtoonkhwa Milli Awami Party ': 'PKMAP',
          'Pashtoonkhawa Milli Awami Party': 'PKMAP',
          'Pashtunkhwa Milli Awami Party ': 'PKMAP',
          # 
          'All Pakistan Muslim League': 'APML',
          #
          'Grand Democratic Allience': 'GDA',
          'G.D.A': 'GDA',
          #
          'Sindh United Party': 'SUP',
          #
          'Qaumi Watan Party': 'QWP',
          "Pakistan Muslim League (Z)":"PML-Z"
          
        }
    df_result_2018['results__party'].replace(replacements, inplace=True)
    
    return df_result_2018


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


df_NA_list = Result_2018()
all_parties = df_NA_list["results__party"].unique().tolist()
party_to_number = {}
i = 0
for party in all_parties:
    print(party,i)
    party_to_number[party] = i                   
    i +=1               
print(party_to_number)    


constituencies = df_NA_list["seat"].unique()
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
    predicted_party = pred_result["Party"].tolist()[0]
    array = [constituency_cordinate_X,constituency_cordinate_Y,original_party,party_to_number[original_party]]
    dic[constituency] = array
       

original_party = "Election Delyaed"      
dic["NA-63"]= [0,0,original_party,0]

original_party = "Election Delyaed"      
dic["NA-103"]= [0,0,original_party,0]




with open( os.path.join("results","result.json"), "w") as write_file:
            json.dump(dic, write_file)