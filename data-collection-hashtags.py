import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from datetime import datetime
import pandas as pd

#Credenciales para utilizar la API de Twitter
consumer_key = 'XXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXX'



#Comprueba si un tweet es un retweet
def checkRT(tweet):
    return hasattr(tweet, 'retweeted_status')

#Funcion la cual segun el analisis sentimental lanza un tweet en rojo o en verde
def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth.secure = True
    api = tweepy.API(auth)
    tweet_ids=[]
    hashtags=[]
    from_date=format(datetime.now(), '%Y-%m-%d')
    query="abb"#+str(from_date)
    cont=0
    for idx,tweet_info in enumerate(tweepy.Cursor(api.search,tweet_mode='extended',count=100,q=query).items()):
        if(not checkRT(tweet_info)):
            for i in range(len(tweet_info.entities['hashtags'])):
                hashtags.append(tweet_info.entities['hashtags'][i]['text'])
                tweet_ids.append(tweet_info.id)
                print(idx)    

    data = {
     'tweet_ids': tweet_ids,
     'hashtags':hashtags
     }
    df = pd.DataFrame.from_dict(data)
    df.to_csv("abb-hashtags.csv",index=False)
    

if  __name__=='__main__':
    main()