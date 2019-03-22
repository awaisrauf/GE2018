# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 13:24:11 2019

@author: ss
"""

import numpy as np
from predict import predict_random,predict_gallup, predict_dunya,predict_partyHistory,predict_districtHistory,predict_twitter
from preprocessing import NA_list_preprocessed
from bayes_opt import BayesianOptimization
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.optimize import linprog

#from tqdm import tqdm

# =============================================================================
# maximum dimension of A matrix
# =============================================================================
def max_dim_A():
    max_dim_A = 0
    df_NA_list = NA_list_preprocessed()    
    # Results Data Frame
    winner_names = ["Imran Ahmed Khan Niazi","IMRAN AHMED KHAN NIAZI","Imran Ahmed Khan Niazi","Imran Ahmad Khan Niazi","Mian Muhammad Shehbaz Sharif","Parvez Elahi","Bilawal Bhutto Zerdari","Chaudhary Nisar Ali Khan","Ahsan iqbal chaudhary","Asif Ali Zadari","Muhammad Hamza Shehbaz Sharif"]
    constituencies = ["NA-53","NA-95","NA-243","NA-35","NA-132","NA-65","NA-200","NA-59","NA-78","NA-213","NA-124"]
    for k in range(len(winner_names)) :  
        constituency,winner_name = constituencies[k],winner_names[k]
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["Constituency Number (ID)"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
        y_output = (current_constituency_data["Name of candidate"]==winner_name).tolist()
        y_output = np.array(y_output).astype(int)
        if y_output.shape[0]>max_dim_A:
            max_dim_A = y_output.shape[0]

        return max_dim_A

# =============================================================================
# 
# =============================================================================
def matrix_A():
    para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11 = 1,1,1,1,1,1,1,1,1,1,1,1
    df_NA_list = NA_list_preprocessed()    
    # Results Data Frame
    winner_names = ["Imran Ahmed Khan Niazi","IMRAN AHMED KHAN NIAZI","Imran Ahmed Khan Niazi","Imran Ahmad Khan Niazi","Mian Muhammad Shehbaz Sharif","Parvez Elahi","Bilawal Bhutto Zerdari","Chaudhary Nisar Ali Khan","Ahsan iqbal chaudhary","Asif Ali Zadari","Muhammad Hamza Shehbaz Sharif"]
    constituencies = ["NA-53","NA-95","NA-243","NA-35","NA-132","NA-65","NA-200","NA-59","NA-78","NA-213","NA-124"]
    
    A = np.zeros([12,max_dim_A()*11])
    Y = np.zeros([374,1])
    for k in range(len(winner_names)) :  
        constituency,winner_name = constituencies[k],winner_names[k]
        # slice data for one constituency
        is_relevant_constituency = df_NA_list["Constituency Number (ID)"] == constituency
        current_constituency_data = df_NA_list[is_relevant_constituency]
        y_output = (current_constituency_data["Name of candidate"]==winner_name).tolist()
        y_output = np.array(y_output).astype(int)
        y_output_paded = np.zeros([34,1])
        y_output_paded[:y_output.shape[0]] = y_output.reshape(-1,1)
        Y[k:k+34,:] = y_output_paded
        can = np.zeros([12,y_output.shape[0]])
        # predict
        can[0]=  para0*np.array(predict_dunya(current_constituency_data))
        result_file_name = ["Gallup_2017_1.csv","Gallup_2017_2.csv","Gallup_2018_1.csv","Gallup_2018_2.csv","IPOR_2018_1.csv"]
        can[1] = para1*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[0]))
        can[2] = para2*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[1]))
        can[3] = para3*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[2]))
        can[4] = para4*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[3]))
        can[5] = para5*np.array(predict_gallup(current_constituency_data, survey_name = result_file_name[4]))
        can[6] = para6*np.array(predict_partyHistory(current_constituency_data))

        result_file_name = ["results_1997.csv","results_2002.csv","results_2008.csv","results_2013.csv"]
        can[7] =  para7*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[0]))
        can[8] =  para8*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[1]))
        can[9]=  para9*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[2]))
        can[10] =  para10*np.array(predict_districtHistory(current_constituency_data, file_name=result_file_name[3]))
        can[11] = para11*np.array(predict_twitter(current_constituency_data))
        A[:can.shape[0],:can.shape[1]] = can
        A =  np.nan_to_num(A,0)
    return A,Y
# =============================================================================
# solves ||y-Ax||2 with pseudo inverse
# =============================================================================
def l2_Exact():
    A,Y = matrix_A()
    A_inv = np.linalg.pinv(np.matmul(A.T,A))
    A_s = np.matmul(A_inv,A.T)
    x = np.matmul(A_s.T,Y)
    x = x/np.abs(x).sum()   
    return x

# =============================================================================
# solves ||y-Ax||1 with linear programming
# =============================================================================
def l1_LP():
    A,Y = matrix_A()
    
    
    M1 = np.concatenate((-A,-np.eye(A.shape[0],A.shape[1])),1)
    M2 = np.concatenate((A,-np.eye(A.shape[0],A.shape[1])),1)
    M = np.concatenate((M1,M2),0).T
    M = M+0.0001
    
    para0= (0.5,1)
    para1 = (0.01,0.1)
    para2 = (0.01,0.1)
    para3 =  (0.01,1)
                                          
    para4 =  (0.01,1)
    para5 =(0.01,1)
    para6 =  (0.01,1)
    para7 = (0.01,0.2)
    
    para8 = (0.01,0.3)
    para9 = (0.1,0.4)
    para10 = (0.1,0.5)
    para11 =(0.01,0.1)
    c0_bounds = (None, None)
    c1_bounds = (None, None)
    c2_bounds = (None, None)
    c3_bounds = (None, None)
    c4_bounds = (None, None)
    c5_bounds = (None, None)
    c6_bounds = (None, None)
    c7_bounds = (None, None)
    c8_bounds = (None, None)
    c9_bounds = (None, None)
    c10_bounds = (None, None)
    c11_bounds = (None, None)
    
    bounds = (c0_bounds,c1_bounds,c2_bounds,c3_bounds,c4_bounds,c5_bounds,c6_bounds,c7_bounds,c8_bounds,c9_bounds,c10_bounds,c11_bounds,para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11)
    
    b = np.concatenate((Y,-Y),0)
    c=np.concatenate((np.zeros([12,1]),np.ones([12,1])),0).reshape(-1)
    presolve=False
    x = linprog(c,M,b,bounds=bounds)#,method="interior-point")
    x_optim = x['x'][12:]
    return x_optim
