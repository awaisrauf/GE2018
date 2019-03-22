# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 14:55:43 2019

@author: ss
"""

from thesis import matrix_A
import numpy as np


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
