# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:33:57 2018

@author: Spider Lab
"""
from textblob import TextBlob
from translation import google



# Tranlates from Urdu to English       
def Translate_En_2_Ur(tweet_text):
    try:
        translated_tweet_text = google(tweet_text, dst = 'en')
    except:
        try:
            en_blob = TextBlob(tweet_text)
            translated_tweet_text = en_blob.translate(to='en').string
        except: 
            translated_tweet_text = ''
    return translated_tweet_text

if __name__ == "__main__":
    tweet_text = '-اگر تم حالات سے خوفزدہ نہیں ہوتو زندہ ہو ورنہ مردہ'
    print(Translate_En_2_Ur(tweet_text))