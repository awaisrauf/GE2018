# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:35:07 2018

@author: Spider Lab
"""
from analysis import tweet_analysis
from matplotlib import pyplot as plt
from utils import Save_as_JSON, Data_Conversion_Party_2_Attributes
import datetime
from tzlocal import get_localzone # to get local date
import json
import numpy as np

number_parties = 4
number_attributes = 6
local = get_localzone()
now = datetime.datetime.now(local)

def Election_Results(save_folder,Tweets_per_Party=5000 , Location = None):
    
    # Important Constituncies Names shoudl also be added
    PTI  = ['PTI', 'Tehreek-e-Insaf', 'Vote4Bat','Imran Khan','IK']
    PMLN = ['PMLN','PML-N',"Vote4Sher", 'Nawaz Sharif', 'MNS','Maryam Nawaz Sharif', 'Shehbaz Sharif','Ahsan Iqbal','N League', 'Punjab', 'Lahore']
    PPP  = ['PPP','Pakistan People Party ','Vote4Teer', 'BBhuttoZardari','Zardari', 'Benazir']
    MQM  = ['MQM','Muttahida Qaumi Movement','APMSO','Vote4Kite']
    #MMA  = ['MMA', 'JUIF','JUI-F','JI','Jamat-e-Islami','Siraj ul Haq', 'Fuzal ur Rehman','Muttahida Majlis-e-Amal', 'FATA']
    #ANP  = ['ANP','Awami National Party','Awami National Party','Asfandyar Wali Khan ']
    
    Parties  = [PTI ,PMLN , PPP , MQM    ]
    Results_Party_wise = {'PTI':[] ,'PMLN':[] , 'PPP':[] , 'MQM':[]   }    
    
    for Party in Parties:
        print('++++++++++++++++++++++')
        print('Analysing ',Party[0])
        print('++++++++++++++++++++++')
        TC,UrC, PC, NEC, PEC,NeEC = tweet_analysis(Party, maxTweetCount = Tweets_per_Party)
        Results_Party_wise[Party[0]] = [TC,UrC, PC, NEC, PEC,NeEC]
    print('Resuts that will be saved in json file',Results_Party_wise)  
    
 
    attrs = ['NumberTweets', 'UrduTweets','Popularity', 'NegEmotion', 'PosEmotion', 'NeuEmotion']
    # Save Results   
    Results_new = Data_Conversion_Party_2_Attributes(Results_Party_wise)
    save_result_path = 'results/'+save_folder+'/' +'original/'+ str(now.date())+'.json'
    
    Results = {}
    # if file already exists then load the data and sum both.
    try:
        # Load Results from relative file
        with open(save_result_path) as json_data:
            print("File Exists")
            Results_old = json.load(json_data)
        # Sum both of the results
        for attr in attrs:
            Results[attr] = (np.array(Results_old[attr]) + np.array(Results_new[attr])).tolist() 
    except:
        Results = Results_new
        
    Save_as_JSON(save_result_path, Results)
    # Save after making its percentage
    Percentage_Results_Save(Results ,save_folder)    
    
###### #########################################   
def Percentage_Results_Save(Results_dict ,folder): 
    
    data = Results_dict
    attrs = ['NumberTweets', 'UrduTweets','Popularity', 'NegEmotion', 'PosEmotion', 'NeuEmotion']
    assert(type(data) == dict)

    Total = np.ones(number_attributes).astype('float')
    i = 0
    for attr in attrs:
        Total[i] = np.sum( np.abs(np.array( data[attr]) ) )
        i+=1
    Total = np.array(Total)   
 
    NumberTweets = np.zeros(number_parties).astype('float')
    UrduTweets = np.zeros(number_parties).astype('float')
    Popularity = np.zeros(number_parties).astype('float')
    NegEmotion = np.zeros(number_parties).astype('float')
    PosEmotion = np.zeros(number_parties).astype('float')
    NeuEmotion = np.zeros(number_parties).astype('float')
    # Result in percentage    
    NumberTweets = (np.array( data[attrs[0]] ) / Total[0]) *100
    UrduTweets =   (np.array( data[attrs[1]] ) / Total[1]) *100
    Popularity =   (np.array( data[attrs[2]] ) / Total[2]) *100
    NegEmotion =   (np.array( data[attrs[3]] ) / Total[3]) *100
    PosEmotion =   (np.array( data[attrs[4]] ) / Total[4]) *100
    NeuEmotion =   (np.array( data[attrs[5]] ) / Total[5]) *100
                    
    Results = {'NumberTweets':NumberTweets.tolist(), 'UrduTweets':UrduTweets.tolist(),'Popularity':Popularity.tolist(), 'NegEmotion':NegEmotion.tolist(), 
               'PosEmotion':PosEmotion.tolist(), 'NeuEmotion':NeuEmotion.tolist()}
    print(Results)
        
    # Save Results
    save_result_path = 'results/'+folder+'/' +'percentage/'+ str(now.date())+'.json'
    Save_as_JSON(save_result_path, Results)
       
    return save_result_path

    
### Graph Results    
def Results_Graph(Result_path):
    
    ## Load Results from relative file
    with open(Result_path) as json_data:
        Results = json.load(json_data)
    # Retrive variables from dictionary    
    NumberTweets = Results['NumberTweets']
    UrduTweets = Results['UrduTweets']
    Popularity = Results['Popularity']
    PosEmotion = Results['PosEmotion']
    NegEmotion = Results['NegEmotion']
    NeuEmotion = Results['NeuEmotion']
#        
    Parties  = ['PTI' ,'PMLN' , 'PPP' , 'MQM' ]
    plt.bar(Parties,Popularity,0.3)
    plt.savefig('graphs/pop_graph.png', dpi = 300)   
    
    index = np.arange(number_parties)
    bar_width = 0.15
    opacity = 0.4
    fig, ax = plt.subplots()
    rects1 = ax.bar(index, NegEmotion, bar_width,
                alpha=opacity, color='r',
                label='Negative Emotion')

    rects2 = ax.bar(index - bar_width, PosEmotion, bar_width,
                alpha=opacity, color='g',
                label='Positive Emotion')
    rects3 = ax.bar(index + bar_width, NeuEmotion, bar_width,
                alpha=opacity, color='b',
                label='Neutral Emotion')
    rects4 = ax.bar(index + 2*bar_width, NumberTweets, bar_width,
                alpha=opacity, color='y',
                label='Total Tweets')
    rects4 = ax.bar(index + 3*bar_width, UrduTweets, bar_width,
                alpha=opacity, color='',
                label='Urdu Tweets')
    
    ax.set_xlabel('Political Parties')
    ax.set_ylabel('Percentage')
    ax.set_title('Election Trends')
    ax.set_xticks(index + bar_width / 4)
    ax.set_xticklabels(Parties)
    ax.legend()
    
    fig.tight_layout()
    plt.savefig('graphs/emt_graph.png',dpi=200)
    plt.show()
    
# Test    
if __name__ == "__main__":
    pass
    #Election_Results('Experiments',Tweets_per_Party=50)
