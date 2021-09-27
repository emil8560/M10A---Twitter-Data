from twitterscraper import query_tweets
from twitterscraper.query import query_tweets_from_user
import datetime as dt
import pandas as pd


begin_date = dt.date(2021, 9, 25)
end_date = dt.date(2020, 9, 26)


limit = 100
lang = 'english'

#Use this to search a specific user

user = 'realDonaldTrump'
tweets = query_tweets_from_user(user)
df = pd.DataFrame(t.__dict__ for t in tweets)

df = df.loc[df['screen_name'] == user]

df = df['text']

df
