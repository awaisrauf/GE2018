# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 08:56:07 2018
@author: Awais: awaisrauf.github.io
@descrption: Functions related to machine learning used
    
"""

import numpy as np
from predict import predict_random,predict_gallup, predict_dunya,predict_partyHistory,predict_districtHistory,predict_twitter
from preprocessing import NA_list_preprocessed
from bayes_opt import BayesianOptimization
import matplotlib.pyplot as plt
from matplotlib import gridspec
#from tqdm import tqdm

#==============================================================================
# Mimicks final model used. This function is then used to get optimal values of 
# hyperparamertes such that predictions form different sources can be combined.
# Method: Used some constituncies that are being considered as confirm seats 
# to find hyperparamerts
#==============================================================================
def hyper_parameter_optimization(para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12):

    df_NA_list = NA_list_preprocessed()    
    # Results Data Frame
    winner_names = ["Imran Ahmed Khan Niazi","IMRAN AHMED KHAN NIAZI","Imran Ahmed Khan Niazi","Imran Ahmad Khan Niazi","Mian Muhammad Shehbaz Sharif","Parvez Elahi","Bilawal Bhutto Zerdari","Chaudhary Nisar Ali Khan","Ahsan iqbal chaudhary","Asif Ali Zadari","Muhammad Hamza Shehbaz Sharif"]
    constituencies = ["NA-53","NA-95","NA-243","NA-35","NA-132","NA-65","NA-200","NA-59","NA-78","NA-213","NA-124"]
    diff = 0
    for k in range(len(winner_names)) :  
        constituency,winner_name = constituencies[k],winner_names[k]
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["Constituency Number (ID)"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
        y_output = (current_constituency_data["Name of candidate"]==winner_name).tolist()
        y_output = np.array(y_output).astype(int)
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
        candidate_prob += para12*np.array(predict_random(current_constituency_data))
        diff += np.sum(np.abs(np.abs(candidate_prob) - np.abs(y_output)))
        return -1*diff



def hyper_parameter_optimization_l2(para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12):

    df_NA_list = NA_list_preprocessed()    
    # Results Data Frame
    winner_names = ["Imran Ahmed Khan Niazi","IMRAN AHMED KHAN NIAZI","Imran Ahmed Khan Niazi","Imran Ahmad Khan Niazi","Mian Muhammad Shehbaz Sharif","Parvez Elahi","Bilawal Bhutto Zerdari","Chaudhary Nisar Ali Khan","Ahsan iqbal chaudhary","Asif Ali Zadari","Muhammad Hamza Shehbaz Sharif"]
    constituencies = ["NA-53","NA-95","NA-243","NA-35","NA-132","NA-65","NA-200","NA-59","NA-78","NA-213","NA-124"]
    diff = 0
    for k in range(len(winner_names)) :  
        constituency,winner_name = constituencies[k],winner_names[k]
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["Constituency Number (ID)"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
        y_output = (current_constituency_data["Name of candidate"]==winner_name).tolist()
        y_output = np.array(y_output).astype(int)
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
        candidate_prob += para12*np.array(predict_random(current_constituency_data))
        diff += np.sum(np.power((candidate_prob- y_output),2))
        return -1*diff  
#==============================================================================
# Uses bayesian optimization find hyper paramertes function
# hyper_parameter_optimization() has minimum value
#==============================================================================
def parameter_serach(iters=1,norm="l1"):  

    # creates an instace with search range of parameters
    if norm == "l2":
        bo = BayesianOptimization(hyper_parameter_optimization_l2,
                                  pbounds={"para0": [0.5,1],"para1": [0.01,0.1],"para2": [0.01,0.1],"para3": [0.01,1],
                                           "para4": [0.01,1],"para5": [0.01,1],"para6": [0.01,1],"para7": [0.01,0.2],
                                           "para8": [0.01,0.3],"para9": [0.1,0.4],"para10": [0.1,0.5],"para11":[0.01,0.1],"para12":[0.01,0.05]},
                                  verbose=0)
    else:
        bo = BayesianOptimization(hyper_parameter_optimization,
                                  pbounds={"para0": [0.5,1],"para1": [0.01,0.1],"para2": [0.01,0.1],"para3": [0.01,1],
                                           "para4": [0.01,1],"para5": [0.01,1],"para6": [0.01,1],"para7": [0.01,0.2],
                                           "para8": [0.01,0.3],"para9": [0.1,0.4],"para10": [0.1,0.5],"para11":[0.01,0.1],"para12":[0.01,0.05]},
                                  verbose=0)        

    bo.maximize(init_points=2, n_iter=iters, acq="ucb", kappa=1)
    # retrive parameters
    hyperparas = bo.max
    para0 = hyperparas["params"]["para0"]
    para1 = hyperparas["params"]["para1"]
    para2 = hyperparas["params"]["para2"]
    para3 = hyperparas["params"]["para3"]
    para4 = hyperparas["params"]["para4"]
    para5 = hyperparas["params"]["para5"]
    para6 = hyperparas["params"]["para6"]
    para7 = hyperparas["params"]["para7"]
    para8 = hyperparas["params"]["para8"]
    para9 = hyperparas["params"]["para9"]
    para10 = hyperparas["params"]["para10"]
    para11 = hyperparas["params"]["para11"]
    para12 = hyperparas["params"]["para12"]
    
#    para0 = hyperparas["max_params"]["para0"]
#    para1 = hyperparas["max_params"]["para1"]
#    para2 = hyperparas["max_params"]["para2"]
#    para3 = hyperparas["max_params"]["para3"]
#    para4 = hyperparas["max_params"]["para4"]
#    para5 = hyperparas["max_params"]["para5"]
#    para6 = hyperparas["max_params"]["para6"]
#    para7 = hyperparas["max_params"]["para7"]
#    para8 = hyperparas["max_params"]["para8"]
#    para9 = hyperparas["max_params"]["para9"]
#    para10 = hyperparas["max_params"]["para10"]
#    para11 = hyperparas["max_params"]["para11"]
#    para12 = hyperparas["max_params"]["para12"]
    paras = [para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12]
    return paras


if __name__ == "__main__": 
    pass
    #para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11,para12 = parameter_serach(iters=9)
