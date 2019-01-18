import pandas as pd 
from termcolor import colored
import pymongo

df_hash=pd.read_csv('abb_hashtags.csv')
df=pd.read_csv('abb.csv',lineterminator='\n')

MONGO_CLIENT = pymongo.MongoClient('XXXXXXXXXXX')
DATABASE = MONGO_CLIENT["XXXXXXXXXXX"]
COLLECTION = DATABASE["XXXXXXXXXXXXXXX"]

def get_most_repeated_hashtags():
    return df_hash['hashtags'].value_counts().index.tolist()[0:20]

def get_tweetids_from_hashtag(hashtag):
    tweetids=[]
    for j in range(len(df_hash['hashtags'])):
        if(hashtag==df_hash['hashtags'][j]):
            tweetids.append(df_hash['tweet_ids'][j])
    return tweetids

def avg_sentiment_per_hashtag(hashtag):
    tweetids=get_tweetids_from_hashtag(hashtag)
    sentiment_score=0
    cont=0
    for tweetid in tweetids:
        for i in range(len(df['tweet_ids'])):
            if(tweetid==df['tweet_ids'][i]):
                cont=cont+1
                sentiment_score=sentiment_score+df['sentiment_score'][i]
    if(cont==0): 
        cont=1
    return sentiment_score/cont

def classify_hashtags():
    hashtags=get_most_repeated_hashtags()
    avg_sentiments=[]
    for hashtag in hashtags:
        print(hashtag)
        avg_sentiments.append(avg_sentiment_per_hashtag(hashtag))
    return {'hashtag':hashtags,'sentiment':avg_sentiments}      

def print_hashtags():
    classified_hashtags=classify_hashtags()
    for i in range(len(classified_hashtags['hashtag'])):
        if(classified_hashtags['sentiment'][i]>0.0):
            colored_text=colored(str(classified_hashtags['hashtag'][i])+" "+ str(classified_hashtags['sentiment'][i]),'green')
        else:
            if(classified_hashtags['sentiment'][i]==0.0):
                colored_text=colored(str(classified_hashtags['hashtag'][i])+" "+ str(classified_hashtags['sentiment'][i]),'blue')
            else:
                colored_text=colored(str(classified_hashtags['hashtag'][i])+" "+ str(classified_hashtags['sentiment'][i]),'red')
        print(colored_text)

if __name__=='__main__':
    print_hashtags()
    COLLECTION.insert_one(classify_hashtags())