# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:35:07 2018

@author: Spider Lab
"""
from analysis import tweet_analysis
import datetime

def Todays_Results(Tweets_per_Party=45000):
    now = datetime.datetime.now()
    PTI  = ['PTI', 'Tehreek-e-Insaf', 'Imran Khan']
    PMLN  = ['PMLN','PML-N', 'Nawaz Sharif', 'Maryam Nawaz Sharif', 'Shehbaz Sharif']
    PPP  = ['PPP', 'Bilawal Bhutto','Zardari', 'Benazir Bhutto']
    MQM  = ['MQM','Muttahida Qaumi Movement','MQM-P', 'Altaf Hussain','Khalid Maqbool Siddiqui','Farooq Sattar']
    MMA  = ['MMA', 'JUI-F','JI','Jamat-e-Islami','Siraj ul Haq', 'Molana Fuzal Ur Rehman','Muttahida Majlis-e-Amal']
    ANP  = ['ANP','Awami National Party','Asfandyar Wali Khan ',' Bacha Khan', 'Khan Abdul Wali Khan']
    
    Parties  = [PTI ,PMLN , PPP , MQM  ,MMA , ANP ]
    Results = {'PTI':[] ,'PMLN':[] , 'PPP':[] , 'MQM':[]  ,'MMA':[] , 'ANP':[]}
    save_result_file = 'results_' + str(now)+'.txt'
    
    
    for Party in Parties:
        print('Analysing ',Party[0])
        TC, PC, NEC, PEC,NeEC = tweet_analysis(Party, maxTweetCount = Tweets_per_Party)
        Results[Party[0]] = [TC, PC, NEC, PEC,NeEC]
    # Save Results    
    file = open(save_result_file, "w")
    file.write( Results )
    file.close()
    print('Results Saved in ', save_result_file)
def Results_Graph(Result_Dictionary):
    

# Test    
if __name__ == "__main__":
    Todays_Results(Tweets_per_Party=1000)