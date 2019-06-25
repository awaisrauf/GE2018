# -*- coding: utf-8 -*-
"""
@author: Awais
@descrption: This file contains all the functions that assigns probabilities to individual constituencies 
             based on different data sources. Second part of function shows data source such as predict_gallup 
             predicts based on different gallup surveys. Output is a list of lenght equal to number of candidate
             eg. [0.1,0.4,0.5]
"""

import numpy as np
import pandas as pd
import os
import json


#==============================================================================
# predicts randomly
#==============================================================================
def predict_random(constituency_data):
    no_candidates = len(constituency_data[constituency_data.columns[0]])   
    probs = np.random.dirichlet(np.ones(no_candidates)*1000.,size=1).tolist()[0]
    return probs


#==============================================================================
# predicts based on gallup and ipor surveys
#==============================================================================
def predict_gallup(constituency_data, survey_name = "Gallup_2018_1.csv"):
    df_gallup_survey = pd.read_csv(os.path.join(".\data\Gallup_Surveys\\",survey_name))
    constituency_number = constituency_data["Constituency Number (ID)"].iloc[0]
    constituency_number = str(constituency_number).split(" ")[0]
    province = constituency_data["Province"].iloc[0]
    # all the parties contesting in the specific constituency
    list_parties = constituency_data["Party Affiliation"].tolist()
    
    # find probability of winning for each candidate from gallup or ipor survey
    candidate_prob = []
    for party in list_parties:
        party_popularity = df_gallup_survey[df_gallup_survey["Party"] == party][province].tolist()
        # if party is not in gallup survey then output is empty list
        is_in_gallup = (df_gallup_survey[df_gallup_survey["Party"].isin([party])].index).tolist()
        # if party is in gallup (not not empty list is false)
        if( not not is_in_gallup ):
            votes = party_popularity[0]/100
            votes = float(votes)                                       
            candidate_prob.append(votes)
        # if not in gallup then zero probability(later replaced by equal values)    
        else:
            candidate_prob.append(0)
            
    # all the candidates that are not in gallup will have a equal prob of winning
    remaining_prob = 1 - np.sum(candidate_prob)  
    # total candidates - candidates that had zero prob in pervious loop = reamining candidates
    # 0.5 shows less confidence
    remaining_candidates = len(candidate_prob) - np.count_nonzero(candidate_prob)
    try:
        prob_extra = 0.5*float(remaining_prob/remaining_candidates)
    except RuntimeWarning:    
        prob_extra = 0
    candidate_prob = [prob_extra if(p==0) else p for p in candidate_prob]
    return candidate_prob


#==============================================================================
# Predicts constituency results based on dunya news results
#==============================================================================
def predict_dunya(constituency_data):
    df_dunya_survey = pd.read_csv("data\Gallup_Surveys\Dunya_2018_1.csv")
    # constituency data
    constituency_number = constituency_data["Constituency Number (ID)"].iloc[0]
    constituency_number = str(constituency_number).split(" ")[0]
    list_parties = constituency_data["Party Affiliation"].tolist()
    
    
    if constituency_number in df_dunya_survey["Constituency"].tolist():
        candidate_prob = []
        for party in list_parties:
            try:
                # party populairty in the constituency
                party_popularity = df_dunya_survey[df_dunya_survey["Constituency"]==constituency_number][party].tolist()
                dunya_survey_parties = df_dunya_survey.columns.values.tolist()
                # if party is in survey and dont have popularity=0 (meaning data is not found)
                if( party in dunya_survey_parties and party_popularity!=0):
                    votes = party_popularity[0]/100
                    votes = float(votes)                                       
                    candidate_prob.append(votes)
                # if not in gallup then zero probability(later replaced by equally probable values)    
                else:
                    candidate_prob.append(0)
            except:
                candidate_prob.append(0)
         # all the candidates that are not in gallup will have a equal prob of winning
        remaining_prob = 1 - np.sum(candidate_prob)  
        # total candidates - candidates that had zero prob in pervious loop = reamining candidates
        remaining_candidates = len(candidate_prob) - np.count_nonzero(candidate_prob)
        try:
            prob_extra = 0.5*float(remaining_prob/remaining_candidates)
        except RuntimeError:
            prob_extra = 0
    
        candidate_prob = [prob_extra if(p==0) else p for p in candidate_prob]
    else:
         candidate_prob = 0.1*np.array(predict_gallup(constituency_data, survey_name = "Gallup_2018_2.csv"))
         candidate_prob = candidate_prob.tolist()
    return candidate_prob

#==============================================================================
# Predict based on party's history in pervious polls
#==============================================================================
def predict_partyHistory(constituency_data):
    df_probability = pd.read_csv("E:\Semester3\GE2018\election\pervious_results_preprocessed\probability.csv")
    list_parties = constituency_data["Party Affiliation"].tolist()
    
    # find probability of winning for each candidate from gallup survey
    candidate_prob = []
    for party in list_parties:
        
        party_prob = df_probability[df_probability["Party"] == party]["Probability"].tolist()
        # if party is in gallup survey or it has zero rating
        is_in_history = (df_probability[df_probability["Party"].isin([party])].index).tolist()
        # if party is in gallup (not not empty list is false)
        if( not not is_in_history ):
            votes = party_prob[0]
            votes = float(votes)                                       
            candidate_prob.append(votes)
        # if not in gallup then zero probability(later replaced by equal values)    
        else:
            candidate_prob.append(0)
            
    # all the candidates that are not in gallup will have a equal prob of winning
    remaining_prob = 1 - np.sum(candidate_prob)  
    # total candidates - candidates that had zero prob in pervious loop = reamining candidates
    remaining_candidates = len(candidate_prob) - np.count_nonzero(candidate_prob)
    try:
        prob_extra = 0.5*float(remaining_prob/remaining_candidates)
    except RuntimeError:
        prob_extra = 0

    candidate_prob = [prob_extra if(p==0) else p for p in candidate_prob]
    return candidate_prob


#==============================================================================
# Predicts based on party's history in the specific constituency
#==============================================================================
def predict_districtHistory(constituency_data, file_name="results_2008.csv"):
    df_district_histroy = pd.read_csv(os.path.join( "E:\Semester3\GE2018\election\pervious_results_preprocessed",file_name))
    # constituency data
    district_name = constituency_data["District"].iloc[0]
    list_parties = constituency_data["Party Affiliation"].tolist()
    
    if district_name in df_district_histroy["District"].tolist():
        candidate_prob = []
        try:
            for party in list_parties:
                history_parties = df_district_histroy.columns.values.tolist()
                # if party is in survey and dont have popularity=0 (meaning data is not found)
                if( party in history_parties):
                    # party populairty in the constituency
                    party_popularity = df_district_histroy[df_district_histroy["District"]==district_name][party].tolist()
                    votes = party_popularity[0]
                    votes = float(votes)      
                    candidate_prob.append(votes)
                # if not in histroy then zero probability(later replaced by equally probable values)    
                else:
                    candidate_prob.append(0)
        except:
              candidate_prob.append(0)
        # all the candidates that are not in gallup will have a equal prob of winning
        remaining_prob = 1 - np.sum(candidate_prob)  
        # total candidates - candidates that had zero prob in pervious loop = reamining candidates
        remaining_candidates = len(candidate_prob) - np.count_nonzero(candidate_prob)
        try:
            prob_extra = 0.5*float(remaining_prob/remaining_candidates)
        except RuntimeWarning:
            prob_extra = 0
    
        candidate_prob = [prob_extra if(p==0) else p for p in candidate_prob]
    else:
        candidate_prob = predict_gallup(constituency_data, survey_name = "Gallup_2018_2.csv")
    return candidate_prob
#==============================================================================
# predicts based on twitter data retrived from another program
#==============================================================================
def predict_twitter(constituency_data):
    
    #  compute popularity from twitter's data already computed and resides in a json file
    with open("data/twitter/pakistan.json") as json_data:
        results = json.load(json_data)
    PTI = results["PTI Line"]
    PMLN = results["PMLN Line"]
    PPPP = results["PPP Line"]
    PTI_score = 0
    PMLN_score = 0
    PPPP_score = 0
    for i in range(len(PTI)):
        PTI_score = 0.1*(i+1)*PTI[i]
        PMLN_score = 0.1*(i+1)*PMLN[i]
        PPPP_score = 0.1*(i+1)*PPPP[i]
    PPPP_score +=20
    total = PTI_score + PMLN_score + PPPP_score
    PTI_pop = PTI_score/total
    PMLN_pop = PMLN_score/total
    PPPP_pop = PPPP_score/total  
    
    # assigns probability if candidate is from three parties mentioned otherwise assigns zero probability
    candidate_prob = []
    for party in constituency_data["Party Affiliation"].tolist():
        if party in ["PTI","PML-N","PPPP"]:
            if(party=="PTI"):
                candidate_prob.append(PTI_pop)
            elif(party=="PML-N"):
                candidate_prob.append(PMLN_pop)
            elif(party=="PPPP"):
                candidate_prob.append(PPPP_pop)
        else:
            candidate_prob.append(0)
    return candidate_prob


if __name__ == "__main__":
    pass
