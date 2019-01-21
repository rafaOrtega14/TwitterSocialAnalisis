import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import pandas as pd

#Credenciales para utilizar la API de Twitter
consumer_key = 'XXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXX'

#Credenciales para utilizar la API de Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "XXXXXXXXXXXXXXXX"
client = language.LanguageServiceClient()

#word search idea

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
    sentiment_scores=[]
    sentiment_magnitudes=[]
    retweets=[]
    favs=[]
    locations=[]
    username=[]
    time=[]
    tweets=[]
    hashtags=[]
    urls=[]
    tweet_ids_hashtags=[]
    tweet_ids_urls=[]
    langs=[]
    cont=0
    for tweet_info in tweepy.Cursor(api.search,tweet_mode='extended',count=100,q='yumi').items():
        if(not checkRT(tweet_info)):
            cont=cont+1
            tweet=tweet_info.full_text
            sentiment_result=tweetAnalizer(tweet)
            sentiment_score=sentiment_result['sentiment_score']
            sentiment_magnitude=sentiment_result['sentiment_magnitude']
            tweet_ids.append(tweet_info.id)
            sentiment_scores.append(sentiment_score)
            sentiment_magnitudes.append(sentiment_magnitude)
            retweets.append(tweet_info.retweet_count)
            favs.append(tweet_info.favorite_count)
            locations.append(tweet_info.user.location)
            tweets.append(tweet_info.full_text)
            langs.append(tweet_info.lang)
            username.append(tweet_info.user.screen_name)
            time.append(tweet_info.created_at)
            for i in range(len(tweet_info.entities['hashtags'])):
                hashtags.append(tweet_info.entities['hashtags'][i]['text'])
                tweet_ids_hashtags.append(tweet_info.id)
            for j in range(len(tweet_info.entities['urls'])):
                urls.append(tweet_info.entities['urls'][j]['url'])
                tweet_ids_urls.append(tweet_info.id)
            print(cont)

    data = {
     'tweet_ids': tweet_ids,'sentiment_score':sentiment_scores,'sentiment_magnitude':sentiment_magnitudes, 
     'retweets': retweets,'favs': favs,'location': locations, 'date': time, 'username': username,'tweet':tweets,
     'langs':langs
     }
    data_hashtags = {
        'tweet_ids': tweet_ids_hashtags,
        'hashtags':hashtags
     }
    data_urls = {
        'tweet_ids': tweet_ids_urls,
        'urls': urls
     }

    df = pd.DataFrame.from_dict(data)
    df_hashtags=pd.DataFrame.from_dict(data_hashtags)
    df_urls=pd.DataFrame.from_dict(data_urls)

    df.to_csv("yumi.csv",index=False)
    df_hashtags.to_csv("yumi_hashtags.csv",index=False)
    df_urls.to_csv("yumi_urls.csv",index=False)

    

if  __name__=='__main__':
    main()