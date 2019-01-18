import pandas as pd 
import requests
import pymongo
import json

#leemos el csv que hemos minado anteriormente gracias al script data-collection
df=pd.read_csv('abbV2.csv',lineterminator='\n')

#Credenciales de la base de datos
MONGO_CLIENT = pymongo.MongoClient('XXXXXXXXXXXXXXXX')
DATABASE = MONGO_CLIENT['XXXXXXXXXXXXXXXX']
COLLECTION = DATABASE['XXXXXXXXXXXXXXX']

#Selecciona los usuarios con maxima difusion teniendo en cuenta favs y RTS
def get_users_max_difussion():
    return df.sort_values(by=['retweets','favs'],ascending=False).head(20).drop_duplicates(subset=['username']).reset_index()

#Hace una media de sentimentos de los tweets de todos los usuarios con maxima difusion
def get_sentiment_avg_rt_fav_by_users(users):
    sentiment_avg=[]
    rt_count=[]
    fav_count=[]
    for user in users['username']:
        cont=0
        elem_sum=0
        rts=0
        favs=0
        for i in range(len(df['location'])):
            if(df['username'][i]==user):
                cont=cont+1
                rts=rts+df['retweets'][i]
                favs=favs+df['favs'][i]
                elem_sum=elem_sum+float(df['sentiment_score'][i])
        rt_count.append(rts)
        fav_count.append(favs)
        sentiment_avg.append(elem_sum/cont)
    return {'sentiment_avg':sentiment_avg,'retweets':rt_count,'favs':fav_count}

#Clasifica los usuarios segun la media de sentimiento 
def classify_users(users):
    userstats=get_sentiment_avg_rt_fav_by_users(users)
    sentiment=userstats['sentiment_avg']
    retweets=userstats['retweets']
    favs=userstats['favs']
    bad_users=[]
    good_users=[]
    neutral_users=[]
    for i in range(len(sentiment)):
        if(sentiment[i]>0.2):
            good_users.append({'username':users['username'][i],'retweets':str(retweets[i]),'favs':str(favs[i])})
        else:
            if(sentiment[i]==0.0):
                bad_users.append({'username':users['username'][i],'retweets':str(retweets[i]),'favs':str(favs[i])})
            else:
                neutral_users.append({'username':users['username'][i],'retweets':str(retweets[i]),'favs':str(favs[i])})
    return {
        'positive_trend_setters': good_users,
        'negative_trend_setters':bad_users,
        'neutral_trend_setters':neutral_users
        }

if __name__=='__main__':
    users=get_users_max_difussion()
    clasified_users=classify_users(users)
    COLLECTION.insert({'trend-setters':clasified_users,'user':'abb','social-network':'twitter'})
    print(clasified_users);