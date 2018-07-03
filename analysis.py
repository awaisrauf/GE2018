# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 02:44:09 2018

@author: Spider Lab
"""

import tweepy 
from textblob import TextBlob
from translation import google
from utils import Translate_En_2_Ur

# Given a tweet data object reterived from twitter api, this will return popularity score    
def tweet_analysis(searchQueries, maxTweetCount = 45000):  
    #access_token	= '761224452-TNVgkYbrSH5UgE3ATZZrgs7vdvk3Bfzq4EruXoRh'
    #access_token_secret = 'mDi0z5wYRBJiNXZONCCfqO3kWeuwVb1FYV6GlLnKTgEF9'
    
    consumer_key = 	'1jWvoRUhffZvJnFm22pqHy5gA'
    consumer_secret ='8F07pwmZVusewI4qa9JpnVw2OMmGRVjvHflkFjMhntZfWpT5um'
    
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    # Maximum number of tweets to be scrapped for queries
    maxTweets = int(maxTweetCount/len(searchQueries)) 
    tweetsPerQry = 100  # this is the max the API permits
    
    
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None
    
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = 0
    
    tweetCount = 0
    popCount = 0 
    negEmotionCount = 0 
    posEmotionCount = 0
    neuEmotionCount = 0
    print("Analysing maximum of {0} tweets".format(maxTweets))
    for searchQuery in searchQueries:
        # Download tweets, 100 at a time
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, result_type = 'recent')
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId,result_type = 'recent')
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),result_type = 'recent')
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId, result_type = 'recent')
                if not new_tweets:
                    print("No more tweets found")
                    break
                
                # Tweet analysis
                for tweet in new_tweets:
                    # Translation
                    if tweet.lang == 'ur':
                        tweet_text = Translate_En_2_Ur(tweet.text)
                    else:
                        tweet_text = tweet.text
                        
                    # Analysis    
                    pol, sub = Sentimen_Analysis_Score(tweet_text)      
                    popularity_score = Popularity(pol, sub, tweet.favorite_count,tweet.retweet_count)
                    
                    # Measureing some numbers
                    tweetCount += 1
                    popCount += popularity_score
                    negEmotionCount += (1 if pol <0 else 0)
                    posEmotionCount += (1 if pol>0 else 0) 
                    neuEmotionCount += (1 if pol==0 else 0)
                    
                print(tweetCount,popCount, negEmotionCount, posEmotionCount,neuEmotionCount )
                print("Analyzed {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
                
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break
            
    return tweetCount,popCount, negEmotionCount, posEmotionCount,neuEmotionCount

# returns sentiment analysis score
def Sentimen_Analysis_Score(tweet_text):
    sentence = TextBlob(tweet_text)
    score = sentence.sentiment
    polarity = score.polarity
    subjectivity = score.subjectivity
    return polarity, subjectivity
    


# Incomplete: Only naive implementation
def Popularity(polarity, subjectivity, count_favs, count_retweets):
    score = polarity* subjectivity+ 0.5* count_favs + 0.01* count_retweets
    return score

# Test
if __name__ == "__main__":
    tweet_analysis(['PTI','Imran'], maxTweetCount = 300)