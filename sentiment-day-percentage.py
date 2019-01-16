import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from termcolor import colored
from datetime import datetime, timedelta
import os
import pandas as pd

#Credenciales para utilizar la API de Twitter
consumer_key = '5pfiXUUZ7Z1WzxxyfMOhld8Sd'
consumer_secret = 'wBfedbnuhjiGsimBYcthXgoyoPsKbLfvDSMIQWGSrFJoR68d2j'
access_token = '299670779-UR9EZwULsJAYLWPVCQi7VJrrox6W8HF2qvBtXrnx'
access_token_secret = 'oJvLc47rGUBtwu3NW1xmfagOmeUaxlVJbvYDl4ONDfqJY'

#Credenciales para utilizar la API de Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/rafaelortega/downloads/credenciales.json"
client = language.LanguageServiceClient()

#Funcion para analizar los sentimientos detras de un tweet
def tweetAnalizer(text):
    try:
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment = client.analyze_sentiment(document=document).document_sentiment
        return {'sentiment_score': sentiment.score, 'sentiment_magnitude': sentiment.magnitude}
    except:
        return {'sentiment_score': 0.0, 'sentiment_magnitude': 0.0}


#Funcion que retorna un mensaje con el grado de satisfaccion total
def avgSatisfaction(total_score,Nelements):
    avg_score=total_score/Nelements
    porcentage=round(abs(avg_score)*100,2)
    if(avg_score<0.0):
        print(colored("El porcentaje de insatisfacción es de: "+str(porcentage)+"%",'red'))
    else:
        print(colored("El porcentaje de satisfacción es de: "+str(porcentage)+"%",'green'))


#Comprueba si un tweet es un retweet
def checkRT(tweet):
    return hasattr(tweet, 'retweeted_status')

#Funcion la cual segun el analisis sentimental lanza un tweet en rojo o en verde
def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth.secure = True
    api = tweepy.API(auth)
    total_score=0
    cont=0
    from_date=format(datetime.now(), '%Y-%m-%d')
    query="CocaCola since:"+str(from_date)
    for tweet_info in tweepy.Cursor(api.search,tweet_mode='extended',count=100,q=query).items(50):
        if(not checkRT(tweet_info)):
            tweet=tweet_info.full_text
            sentiment_result=tweetAnalizer(tweet)
            sentiment_score=sentiment_result['sentiment_score']
            sentiment_magnitude=sentiment_result['sentiment_magnitude']
            total_score+=sentiment_score
            cont=cont+1
    avgSatisfaction(total_score,cont)

    

if  __name__=='__main__':
    main()