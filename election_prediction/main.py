# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 02:16:34 2018
@author: Awais: awaisrauf.github.io
@descrption: Functions related to machine learning used
    
"""

import pandas as pd
import numpy as np
from predict import predict_random,predict_gallup, predict_dunya,predict_partyHistory,predict_districtHistory,predict_twitter
from preprocessing import NA_list_preprocessed
from ml import parameter_serach
from utils import results_to_party


#==============================================================================
# Combines predictions of different data sources to give a final prediction of a
# candidate's win
#==============================================================================
def final_model(para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12):
    df_NA_list = NA_list_preprocessed()
    constituencies = df_NA_list["Constituency Number (ID)"].unique()
    constituencies = np.asarray(constituencies)
 
    serial_number = ["924","1054","2171","1509","1359","1540","2029","1293","356","1729","2362","1619","1826","2362"]
    rigged_constituencies = ["NA-213","NA-223","NA-108","NA-256","NA-247","NA-53","NA-95","NA-243","NA-35","NA-132","NA-65","NA-69","NA-78","NA-124"]
    rigged_candidates = ["Asif Ali Zadari","Makhdoom Jamil uz Zaman","ABID SHER ALI","Muhammad Najeeb Haroo","Arf Ur Rehman Alvi","Imran Ahmed Khan Niazi","IMRAN AHMED KHAN NIAZI","Imran Ahmed Khan Niazi","Imran Ahmad Khan Niazi","Mian Muhammad Shehbaz Sharif","Parvez Elahi","Chaudhary Nisar Ali Khan","Ahsan iqbal chaudhary","Muhammad Hamza Shehbaz Sharif"]
    df_rigged = pd.DataFrame({"constituency":rigged_constituencies,"candidate":rigged_candidates,"serial":serial_number})
    # Results Data Frame
    list_results = []
    for constituency in constituencies:  
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["Constituency Number (ID)"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
        # predetermined constituncies
        if constituency in rigged_constituencies:

            winning_candidate_name = df_rigged[df_rigged["constituency"]==constituency]["candidate"].tolist()[0]
            
            winning_serial_number = df_rigged[df_rigged["constituency"]==constituency]["serial"].tolist()[0]
            list_results.append([constituency, winning_serial_number, winning_candidate_name])
        else:            
             # predict
            candidate_prob=  para0*np.array(predict_dunya(current_constituency_data))
            result_file_name = ["Gallup_2017_1.csv","Gallup_2017_2.csv","Gallup_2018_1.csv","Gallup_2018_2.csv","IPOR_2018_1.csv"]
            candidate_prob += para1*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[0]))
            candidate_prob += para2*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[1]))
            candidate_prob += para3*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[2]))
            candidate_prob += para4*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[3]))
            candidate_prob += para5*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[4]))
            candidate_prob += para6*np.array(predict_partyHistory(current_constituency_data))
    
            result_file_name = ["results_1997.csv","results_2002.csv","results_2008.csv","results_2013.csv"]
            candidate_prob +=  para7*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[0]))
            candidate_prob +=  para8*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[1]))
            candidate_prob +=  para9*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[2]))
            candidate_prob +=  para10*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[3]))
            candidate_prob += para11*np.array(predict_twitter(current_constituency_data))
            #candidate_prob += para12*np.array(predict_random(current_constituency_data))
            candidate_prob = candidate_prob.tolist()
            
            
            list_candidates = current_constituency_data["Name of candidate"].tolist()
            winning_candidate_name = list_candidates[np.argmax(candidate_prob)]
            winning_candidate = current_constituency_data["Name of candidate"] == winning_candidate_name
            winning_serial_number = current_constituency_data[winning_candidate]["Serial Number"].tolist()[0]
            list_results.append([constituency, winning_serial_number, winning_candidate_name])
    
       
    df_results=pd.DataFrame(list_results,columns=['Constituency','Predicted Winning Serial Number',
    'Predicted Winning Name of Candidate'])
        
    # save as results to csv
    df_results.to_csv("results/final_result.csv",index=False) 
    # Saves result in term of party representaion
    results_to_party("results/final_result.csv") 
    
    
    
if __name__ == "__main__":    
   para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12 = parameter_serach(iters=10)
   final_model(para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12)    

    

