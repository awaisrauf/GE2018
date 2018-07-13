# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:33:57 2018

@author: Spider Lab
"""
from textblob import TextBlob
import numpy as np
#from translation import google
import tweepy 
import json
import subprocess
import time



# Tranlates from Urdu to English       
def Translate_En_2_Ur(tweet_text):
# Google translatioin api is taking too much tim
# Comprison: with google 5-6 secs without google 1-1.3    
#    try:
#        pass#translated_tweet_text = google(tweet_text, dst = 'en')
#    except:
    try:
        en_blob = TextBlob(tweet_text)
        translated_tweet_text = en_blob.translate(to='en').string
    except: 
        translated_tweet_text = ''
    return translated_tweet_text

def Save_as_JSON(path, data):
    assert(type(data) == dict)
    with open( path, "w") as write_file:
        json.dump(data, write_file)
    print('data saved in ', path) 

'''
Return tweets per Query
'''
def Download_Tweets(searchWord, max_id, sinceId, tweetsPerQry = 100, Location = None):
    # Twitter api access details
    #access_token	= '761224452-TNVgkYbrSH5UgE3ATZZrgs7vdvk3Bfzq4EruXoRh'
    #access_token_secret = 'mDi0z5wYRBJiNXZONCCfqO3kWeuwVb1FYV6GlLnKTgEF9'
    consumer_key = 	'Ew7PN6nn9SxcS1en8Dc3yaAiu'
    consumer_secret ='foUXD1OTcG94tW7HBR0zwqRisXmT3kY6cnH7dQj9njitTPOKdW' 
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    # Local Variables
    
    
    #Download tweets, 100 maximum
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchWord, count=tweetsPerQry, result_type = 'recent',geocode= Location)
            else:
                new_tweets = api.search(q=searchWord, count=tweetsPerQry,
                                        since_id=sinceId,result_type = 'recent',geocode= Location)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchWord, count=tweetsPerQry,
                                        max_id=str(max_id - 1),result_type = 'recent',geocode= Location)
            else:
                new_tweets = api.search(q=searchWord, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId, result_type = 'recent',geocode= Location)
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        new_tweets = 'Error'
    return new_tweets

def Data_Conversion_Party_2_Attributes(data):
    number_parties = 4
    assert(type(data) == dict)
    Parties  = ['PTI' ,'PMLN' , 'PPP' , 'MQM'  ]
    
    
    NumberTweets = np.ones(number_parties).astype('float')
    UrduTweets = np.ones(number_parties).astype('float')
    Popularity = np.ones(number_parties).astype('float')
    NegEmotion = np.ones(number_parties).astype('float')
    PosEmotion = np.ones(number_parties).astype('float')
    NeuEmotion = np.ones(number_parties).astype('float')
    i = 0
    # Result in percentage
    for party in Parties:
        NumberTweets[i] = data[party][0]
        UrduTweets[i] = data[party][1]
        Popularity[i] = data[party][2]
        NegEmotion[i] = data[party][3]
        PosEmotion[i] = data[party][4]
        NeuEmotion[i] = data[party][5]
        i+=1
    
    Results = {'NumberTweets':NumberTweets.tolist(), 'UrduTweets':UrduTweets.tolist(),'Popularity':Popularity.tolist(), 'NegEmotion':NegEmotion.tolist(), 
               'PosEmotion':PosEmotion.tolist(), 'NeuEmotion':NeuEmotion.tolist()}

    return Results
"""
Funciton to run bat file automatically
"""
def run_bat_file():
    filepath="D:\Awais\GE2018\GE2018\prediction_code\automatic_git_push.bat"
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    
    stdout, stderr = p.communicate()
    print (p.returncode) # is 0 if success	

if __name__ == "__main__":
    start = time.clock()
    tweet_text = '-اگر تم حالات سے خوفزدہ نہیں ہوتو زندہ ہو ورنہ مردہ'
    print(Translate_En_2_Ur(tweet_text))
    #your code here    
    print (time.clock() - start)