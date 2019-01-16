import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from termcolor import colored
import os
import pandas as pd

#Credenciales para utilizar la API de Twitter
consumer_key = 'XXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXX

#Credenciales para utilizar la API de Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/rafaelortega/downloads/credenciales.json"

#Funcion para analizar los sentimientos detras de un tweet
def tweetAnalizer(text):
    try:
        client = language.LanguageServiceClient()
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment = client.analyze_sentiment(document=document).document_sentiment
        return {'sentiment_score': sentiment.score, 'sentiment_magnitude': sentiment.magnitude}
    except:
        return {'sentiment_score': 0.0, 'sentiment_magnitude': 0.0}

#Funcion que define si un tweet es neutral
def checkNeutral(sentiment_score,sentiment_magnitude):
    Neutral=False
    if(sentiment_score == 0.0 and (sentiment_magnitude>-0.2 and sentiment_magnitude<0.2)):
        Neutral=True
    return Neutral

#Funcion que retorna un mensaje con el grado de satisfaccion total
def avgSatisfaction(total_score,Nelements):
    avg_score=total_score/Nelements
    porcentage=abs(avg_score)*100
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
    for tweet_info in tweepy.Cursor(api.search,tweet_mode='extended',count=100,q='CocaCola').items(10):
        if(not checkRT(tweet_info)):
            cont=cont+1
            tweet=tweet_info.full_text
            sentiment_result=tweetAnalizer(tweet)
            sentiment_score=sentiment_result['sentiment_score']
            sentiment_magnitude=sentiment_result['sentiment_magnitude']
            if(checkNeutral(sentiment_score,sentiment_magnitude)):
                colored_text=colored(tweet_info.full_text +" "+ str(sentiment_score),'blue')
            else:
                total_score+=sentiment_score
                if(sentiment_score<0.2):
                    colored_text=colored(tweet_info.full_text +" "+ str(sentiment_score),'red')
                else:
                    colored_text=colored(tweet_info.full_text +" "+ str(sentiment_score),'green')
            print(colored_text)
            print("----------------------------")
    avgSatisfaction(total_score,cont)

    

if  __name__=='__main__':
    main()