# -*- coding: utf-8 -*-
"""
@author: Awais
@descrption: run this file to run the model
    
"""

import pandas as pd
import numpy as np
from predict import predict_random,predict_gallup, predict_dunya,predict_partyHistory,predict_districtHistory,predict_twitter
from preprocessing import NA_list_preprocessed
from utils import results_to_party
from tqdm import tqdm
import time
from comparison import accuracy_share_wise, accuracy_seat_wise
from la import l2_Exact, l1_LP
from model import final_model
from comparison import compare_methods
from ml import bo_parameter_serach

# uncomment following line if you want to use Bayesian optimization to find parameters	
# paras = bo_parameter_serach(norm="l1")
# paras = bo_parameter_serach(norm="l2")
# paras = l1_LP()
# paras = l2_Exact()

# hyper parameter values: Taken form bayesian optimization.
para0 = 0.5
para1 = 0.01
para10 = 0.1
para11 = 0.01
para12 = 0.01
para2 = 0.1
para3 = 0.01
para4 = 0.05
para5 = 1.0
para6 = 0.01
para7 = 0.01
para8 = 0.01
para9 = 0.1
paras = [para0,para1,para2,para3,para4,para5,para6,para7,para8,para9,para10,para11]
# Run final model
#final_model(paras[:12])   

# Compare different methods that were tried instead of Bayesian Optimization
# l1 norm: Linear Programming
data1 = compare_methods("L2-EX")
# l2 norm: Bayesian Optimization
data2 = compare_methods("L1-LP")
# l1 norm: Exact solution
data3 = compare_methods("L1-BO")
data4 = compare_methods("L2-BO")
# save results
save_results = pd.DataFrame( [data1,data2,data3,data4],columns = ['Method Name','Seat Level Accuracy','Party Level Accuracy','Time taken'])
save_results.to_csv("compartive_results.csv",sep=";")

    

