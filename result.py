# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:35:07 2018

@author: Spider Lab
"""
from analysis import tweet_analysis
from matplotlib import pyplot as plt
import datetime
import json
import numpy as np

number_parties = 5

def Todays_Results(Tweets_per_Party=45000):
    now = datetime.datetime.now()
    PTI  = ['PTI', 'Tehreek-e-Insaf', 'Imran Khan','KPK']
    PMLN  = ['PMLN','PML-N', 'Nawaz Sharif', 'Maryam Nawaz Sharif', 'Shehbaz Sharif', 'Punjab']
    PPP  = ['PPP', 'Bilawal Bhutto','Asif Ali Zardari', 'Benazir Bhutto', 'Sindh']
    MQM  = ['MQM','Muttahida Qaumi Movement','MQM-P', 'Altaf Hussain','Khalid Maqbool Siddiqui','Farooq Sattar','Karachi']
    MMA  = ['MMA', 'JUI-F','JI','Jamat-e-Islami','Siraj ul Haq', 'Fuzal ur Rehman','Muttahida Majlis-e-Amal']
    #ANP  = ['ANP','Awami National Party','Awami National Party','Asfandyar Wali Khan ']
    
    Parties  = [PTI ,PMLN , PPP , MQM  ,MMA  ]
    Results = {'PTI':[] ,'PMLN':[] , 'PPP':[] , 'MQM':[]  ,'MMA':[] }
    save_result_file = 'results_' + str(now.date())+'.json'
    
    
    for Party in Parties:
        print('++++++++++++++++++++++')
        print('Analysing ',Party[0])
        print('++++++++++++++++++++++')
        TC, PC, NEC, PEC,NeEC = tweet_analysis(Party, maxTweetCount = Tweets_per_Party)
        Results[Party[0]] = [TC, PC, NEC, PEC,NeEC]
    # Save Results    
    with open( save_result_file, "w") as write_file:
        json.dump(Results, write_file)
    print('Results Saved in ', save_result_file)
    
    
###### #########################################   
def Percentage_Results(Result_file): 
    
    with open(Result_File, "r") as read_file:
        data = json.load(read_file)
    assert(type(data) == dict)
    Parties  = ['PTI' ,'PMLN' , 'PPP' , 'MQM'  ,'MMA' ]
    print(data)
    #
    number_attributes = 5
    
    Total = np.ones(number_attributes).astype('float')
    for i in range(number_attributes):
        for party in Parties:    
            Total[i] += data[str(party)][i] 
    print('Total:',Total)    
    # Normalized Results
    NumberTweets = np.ones(number_parties).astype('float')
    Popularity = np.ones(number_parties).astype('float')
    NegEmotion = np.ones(number_parties).astype('float')
    PosEmotion = np.ones(number_parties).astype('float')
    NeuEmotion = np.ones(number_parties).astype('float')
    i = 0
    # Result in percentage
    for party in Parties:
        NumberTweets[i] = (data[party][0]/Total[0])*100
        Popularity[i] = (data[party][1]/Total[1])*100
        NegEmotion[i] = (data[party][2]/Total[2])*100
        PosEmotion[i] = (data[party][3]/Total[3])*100
        NeuEmotion[i] = (data[party][4]/Total[4])*100
        i+=1
    return NumberTweets,Popularity ,NegEmotion, PosEmotion, NeuEmotion

    
### Graph Results    
def Results_Graph(Result_file):
    NumberTweets, Popularity ,NegEmotion, PosEmotion, NeuEmotion = Percentage_Results(Result_file)
    Parties  = ['PTI' ,'PMLN' , 'PPP' , 'MQM'  ,'MMA'  ]

    plt.bar(Parties,Popularity)
    plt.savefig('results/pop_graph.png', dpi = 300)   
    
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
    rects3 = ax.bar(index + bar_width, PosEmotion, bar_width,
                alpha=opacity, color='b',
                label='Neutral Emotion')
    rects4 = ax.bar(index + 2*bar_width, PosEmotion, bar_width,
                alpha=opacity, color='y',
                label='Total Tweets')
    
    ax.set_xlabel('Political Parties')
    ax.set_ylabel('Percentage')
    ax.set_title('Election Trends')
    ax.set_xticks(index + bar_width / 4)
    ax.set_xticklabels(Parties)
    ax.legend()
    
    fig.tight_layout()
    plt.savefig('results/emt_graph.png',dpi=200)
    plt.show()
    
# Test    
if __name__ == "__main__":
    Todays_Results(Tweets_per_Party=1000)
    Result_File = 'results_2018-07-03.json'
    Results_Graph(Result_File)