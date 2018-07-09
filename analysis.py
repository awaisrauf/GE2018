# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 02:44:09 2018

@author: Spider Lab
"""

from textblob import TextBlob
from utils import Translate_En_2_Ur,Download_Tweets
import numpy as np

# Given a tweet data object reterived from twitter api, this will return popularity score    
def tweet_analysis(searchWords, maxTweetCount = 5000, Location = None):  
    #
    # Maximum number of tweets to be scrapped for queries
    maxTweetsPerWord = int(maxTweetCount/len(searchWords)) 
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = 0
    countTweetsTotal = 1  # To avoid divison by zero
    countUrduTweets = 0
    popCount = 0 
    negEmotionCount = 0 
    posEmotionCount = 0
    neuEmotionCount = 0
    
    
    print("Analysing maximum of {0} tweets".format(maxTweetsPerWord))
    for searchWord in searchWords:
        
        countTweetsPerWord = 0
        print('#### Analysing word ', searchWord)
        while countTweetsPerWord < maxTweetsPerWord:
            new_tweets = Download_Tweets(searchWord, max_id, sinceId, Location = Location )
            # To cope with slow internet connection
            while(new_tweets == 'Error'):
                new_tweets = Download_Tweets(searchWord, max_id, sinceId, Location = Location )
                
            if not new_tweets:
                print("No more tweets found")
                break
            
            # Analysis
            for tweet in new_tweets:                    
                # Translation
                if tweet.lang == 'ur':
                    tweet_text = Translate_En_2_Ur(tweet.text)
                    countUrduTweets +=1
                else:
                    tweet_text = tweet.text
                    
                # Analysis    
                pol, sub = Sentimen_Analysis_Score(tweet_text)      
                popularity_score = Popularity(pol, sub, tweet.favorite_count,tweet.retweet_count)
                
                # Measureing some numbers
                countTweetsPerWord += 1
                popCount += popularity_score
                negEmotionCount += (1 if pol <  0   else 0)
                posEmotionCount += (1 if pol >  0   else 0) 
                neuEmotionCount += (1 if pol == 0   else 0)
       
            print("Analyzed {0} tweets".format(countTweetsPerWord))   
            print('One Instance Stats:',countTweetsPerWord, countUrduTweets, popCount,negEmotionCount, posEmotionCount,neuEmotionCount )      
            max_id = new_tweets[-1].id
        countTweetsTotal += countTweetsPerWord 
            
            
        
        print('All Words Stats:',countTweetsTotal,popCount, negEmotionCount, posEmotionCount,neuEmotionCount )
                
        
    # Normalization of results
    popCount, negEmotionCount =  popCount/countTweetsTotal, negEmotionCount/countTweetsTotal
    posEmotionCount, neuEmotionCount = posEmotionCount/countTweetsTotal,neuEmotionCount/countTweetsTotal  
    
    return countTweetsTotal,countUrduTweets, popCount, negEmotionCount, posEmotionCount,neuEmotionCount





# returns sentiment analysis score
def Sentimen_Analysis_Score(tweet_text):
    sentence = TextBlob(tweet_text)
    score = sentence.sentiment
    polarity = score.polarity
    subjectivity = score.subjectivity
    return polarity, subjectivity
    


# Incomplete: Only naive implementation
def Popularity(polarity, subjectivity, count_favs, count_retweets):
    score = (polarity)*(0.02* count_favs + 0.01* count_retweets)
    # More subjective a tweet is, more strong it is for voting patters
    score = subjectivity * score
    return score

# Test
if __name__ == "__main__":
    print(Sentimen_Analysis_Score("I love you bob said the idiot who was so fuckingly idotic"))
    a,b,c,d,e = tweet_analysis(['PTI','ldsfs djfdlsjf jfldsjfldjflsdjf'], maxTweetCount = 100)
    print(a,b,c,d,e)