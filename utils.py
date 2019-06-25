# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 23:14:04 2018
@author: Awais: awaisrauf.github.io
@descrption:  Extra functions  
"""

import numpy as np
import pandas as pd
import os
from preprocessing import Perevious_results_preprocessed,NA_list_preprocessed


#==============================================================================
# Generates populairty of a particular party at district level from perevious 
# election results. Uses 1997, 2002,2007 and 2013 election results 
#==============================================================================

def predict_pervisous_election():
    df_perevious_results = Perevious_results_preprocessed()
    
    # find probability of win for each party in each district for each election
    elections = [1997,2002,2008, 2013]
    for election_year in elections:
        df_year_election_results = df_perevious_results[df_perevious_results["Year"] == election_year]
        list_districts = df_year_election_results["District"].unique().tolist()
        list_parties = df_year_election_results["Party"].unique().tolist()
        # empty results list 
        list_result = []
        
        # for each party in each district, generate a probability of win form perevious results
        for district in list_districts:
            district_data = df_year_election_results[df_year_election_results["District"] == district]
            list_constituencies = district_data["constituency"].unique().tolist()
            district_result = np.zeros(len(list_parties))
            
            # for each constituency in each district
            for constituency in list_constituencies:
                constituency_result = []
                constituency_data = district_data[district_data["constituency"] == constituency]
                constituency_total_votes_cast = int(constituency_data["Votes"].sum())
               
                #
                for party in list_parties:
                    try:
                        party_votes = constituency_data[constituency_data["Party"] == party]["Votes"]
                        party_win_prob = float(party_votes/constituency_total_votes_cast)
                        constituency_result.append(party_win_prob)
                    except:
                        constituency_result.append(0)
                district_result = np.array(district_result) + np.array(constituency_result)
                
            # normalize probabilties    
            district_result = district_result/len(list_constituencies)
            district_result = district_result.tolist()
            list_result.append(district_result)
            
        df_result = pd.DataFrame(list_result, columns=list_parties)
        #df_result.dropna(inplace= True)
        df_result["District"]= list_districts
        df_result.to_csv(os.path.join("pervious_results_preprocessed/","results_"+str(election_year) +".csv" ))         
    return df_result

#==============================================================================
# What is probability of winning  for a specific party's candidiate given if we
# only know his party affiliation. For each party: total number of candidates
# who won / total number candidates who contest election from the party
#==============================================================================
def win_probability():
    df_perevious_results = Perevious_results_preprocessed()
    list_parties = df_perevious_results["Party"].unique().tolist()
    list_win_probs = []
    for party in list_parties:
        # find winners from a party
        winning_candidates =  df_perevious_results["Position"]== "Winner"
        is_party_candidate =  df_perevious_results["Party"] == party
        winning = df_perevious_results[ winning_candidates & is_party_candidate]["Candidate"].count()
        list_win_probs.append(winning/np.sum(is_party_candidate))
    df_win_probability = pd.DataFrame({"Party":list_parties,"Probability":list_win_probs})  
    df_win_probability.to_csv(os.path.join("pervious_results_preprocessed/","probability.csv" ),index=False)


#==============================================================================
# From results, generate two files to show party affiliation and winning party
# distribution
#==============================================================================
def results_to_party(file_path):
    df_result_1 = pd.read_csv(file_path)
    df_NA_list = NA_list_preprocessed()
    
    party_list = []
    for serial_number in df_result_1["Predicted Winning Serial Number"]:
        party = df_NA_list[df_NA_list["Serial Number"] == serial_number]["Party Affiliation"].tolist()[0]
        party_list.append(party)
    
    df_result_1["Party"] = party_list
    df_result_1.to_csv("data\\results/result_party.csv",index=False)
    party_distribution = df_result_1["Party"].value_counts()
    party_distribution.to_csv("data\\results/parties_result.csv",index=True)
    print(party_distribution)
    party_result = df_result_1
    return party_result, party_distribution


    
if __name__ == "__main__":
    pass
    
