# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 06:13:37 2018

@author: Spider Lab
"""
from result import Election_Results, Results_Graph
import time
run_flag = 0
while(run_flag==0):
    start = time.clock()
    Election_Results('Pakistan',Tweets_per_Party=8000)
    # Radius is calculated using A =pi*r^2: assuming perfect circle
    Election_Results('Punjab', Tweets_per_Party = 5000,Location=[31.1704,72.7097,145])
    Election_Results('KPK', Tweets_per_Party = 3000,Location=[34.9526,72.3311,102])
    Election_Results('Sindh', Tweets_per_Party = 4000,Location=[25.8943,68.5247,120])
    Election_Results('Balouchistan', Tweets_per_Party = 2000,Location=[28.4907,65.0958,190])
    Results_Graph('results/KPK/percentage/2018-07-07.json')
    print (time.clock() - start)
    run_flag = 1