import pandas as pd
import numpy as np
import requests, json, re, time, os, ast

from collections import defaultdict

path = 'D:\Projects\Github\games-requirements-checker\datasets\steam_dataset\steamapi\json\ss_details.json'
df = pd.read_csv('D:\Projects\Github\games-requirements-checker\datasets\steam_dataset\steamapi\csv\game_details.csv', sep=',')
# df.to_csv('D:\Projects\Github\games-requirements-checker\datasets\steam_dataset\steamapi\csv\game_details.csv', index=True)
df['appid'] = df['appid'].astype(str)

with open(path, 'r', encoding='UTF-8') as file:
    rfile = json.load(file)

list_of_appids = []
for i in range(len(rfile)):
    list_of_appids.append(list(rfile[i].keys())[0])

def to_pandas(idx, appid):
    if rfile[idx][appid]['success'] == True:
        x = rfile[idx][appid]['data']
    else:
        x = rfile[idx][appid]
    return x

list_of_data = []
for i in range(len(rfile)):
    appid = list_of_appids[i]
    res = to_pandas(i, appid)
    list_of_data.append(res)

# print(list_of_data[:3])
# type(list_of_data[0])
df_details = pd.DataFrame(list_of_data)
df_details = df_details[~df_details['steam_appid'].duplicated()]
df_details = df_details.fillna(0)
# df_details.head(3)
# len(df_details)

#convert IDs to int
df['appid'] = df['appid'].astype(np.int64)
df_details['steam_appid'] = df_details['steam_appid'].astype(np.int64)

# df1_ids = set(df_details['steam_appid'])
# df2_ids = set(df['appid'][:29868])

# x = df2_ids - df1_ids
# print(x)

# df_details.columns
df.drop('Unnamed: 0', axis=1, inplace=True)
df.columns
df_details.columns
df1 = df[['appid', 'developer', 'publisher', 
'score_rank', 'positive', 'negative',
'initialprice', 'discount', 'ccu', 
'languages', 'genre', 'tags']]

df_details = df_details.rename(columns={'steam_appid': 'appid'})
df2 = df_details[['appid', 'name','required_age', 
'is_free','detailed_description', 'about_the_game', 
'short_description', 'header_image', 'website', 
'pc_requirements', 'mac_requirements', 'linux_requirements',
'release_date', 'metacritic']]
# df2['appid'][1] = 100
df2.columns

# df_combined = pd.concat([df1,df2], axis=0).reset_index(drop = True)
df_combined = pd.merge(df1, df2, on='appid')
df_combined.head(3)

df_combined.columns
# df_combined = df_combined[['appid','name', 'release_date', 'developer', 'publisher',
#                             'is_free', 'initialprice', 'languages', 'genre', 
#                             'tags', 'detailed_description', 'about_the_game',
#                             'short_description', 'header_image', 'website', 'pc_requirements',
#                             'mac_requirements', 'linux_requirements']]
df_combined.head(3)
# df_combined.isnull().sum()
# len(df_combined)

df_combined.to_csv('D:/Projects/Github/games-requirements-checker/datasets/steam_dataset/steamapi/csv/steamapp_api.csv', index=False)