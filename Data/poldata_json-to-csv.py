import pandas as pd
import ast 
import numpy as np
import json

with open('poldata_20211005.json', "r") as outfile:
    all_data = json.load(outfile)

df_tweets = pd.DataFrame.from_records(all_data.get('data'))
df_users = pd.DataFrame.from_records(all_data.get('includes').get('users'))

def fix_dicts(string):
    if string is np.nan:
        return(string)
    if not isinstance(string, dict):
        string_as_dict = ast.literal_eval(string)
        return(string_as_dict)
    else:
        return(string)

def unnest_hashtags(entities):
    try:
        hashtags = list(entities.get('hashtags'))
    except:
        return(list())
    if isinstance(hashtags, list):
        hashtags_list = [hashtag.get('tag') for hashtag in hashtags]
        return(hashtags_list)
    else:
        return
    
def unnest_mentions(entities):
    try:
        mentions = list(entities.get('mentions'))
    except:
        return(list())
    if isinstance(mentions, list):
        mentions_list = [mention.get('username') for mention in mentions]
        return(mentions_list)
    else:
        return

def unnest_urls(entities):
    try:
        urls = list(entities.get('urls'))
    except:
        return(list())
    if isinstance(urls, list):
        urls_list = [url.get('username') for url in urls]
        return(urls_list)
    else:
        return
    
def unnest_cashtags(entities):
    try:
        cashtags = list(entities.get('cashtags'))
    except:
        return(list())
    if isinstance(cashtags, list):
        cashtags_list = [cashtag.get('username') for cashtag in cashtags]
        return(cashtags_list)
    else:
        return
       

drop_cols = ['public_metrics', 'entities']

df_tweets['public_metrics'] = df_tweets['public_metrics'].apply(fix_dicts)
df_tweets['entities'] = df_tweets['entities'].apply(fix_dicts)
df_tweets_unnest = pd.concat([df_tweets, pd.json_normalize(df_tweets['public_metrics'])], axis = 1)
df_tweets_unnest['hashtags'] = df_tweets_unnest['entities'].apply(unnest_hashtags)
df_tweets_unnest['mentions'] = df_tweets_unnest['entities'].apply(unnest_mentions)
df_tweets_unnest['urls'] = df_tweets_unnest['entities'].apply(unnest_urls)
df_tweets_unnest['cashtags'] = df_tweets_unnest['entities'].apply(unnest_cashtags)
df_tweets_unnest = df_tweets_unnest.loc[:, ~df_tweets_unnest.columns.isin(drop_cols)]

df_users['public_metrics'] = df_users['public_metrics'].apply(fix_dicts)
df_users_unnest = pd.concat([df_users, pd.json_normalize(df_users['public_metrics'])], axis = 1)
df_users_unnest = df_users_unnest.rename(columns = {'id': 'author_id', 'created_at': 'author_created_at'})
df_users_unnest = df_users_unnest.loc[:, ~df_users_unnest.columns.isin(drop_cols)]

df_combined = pd.merge(df_tweets_unnest, df_users_unnest, how = 'left', left_on = 'author_id', right_on = 'author_id').drop_duplicates(subset = ['id'])
df_combined.to_csv('poldata_20210924.csv', index = False)