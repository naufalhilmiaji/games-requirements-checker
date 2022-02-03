import pandas as pd
import numpy as np
import math, requests, json, re, time, os
from multiprocessing import Pool

from tqdm import tqdm

def get_data(url):
    try:
        print('Loading JSON...')

        data = requests.get(url)
        if data.status_code != 200:
            print(f'Error: {url}')

        jsons = data.json()
        time.sleep(1)
        os.system('cls')
        return jsons

    except Exception as e:
        print(e)

if __name__ == '__main__':
    with open('datasets/steam_dataset/steamapi/json/steamapp_api.json', "r") as file:
        steamapp_api = json.load(file)

    df_game_summaries = pd.read_csv('datasets/steam_dataset/steamapi/csv/game_summaries.csv', sep=',')
    list_of_appids = df_game_summaries['appid'].to_list()

    urls = []

    print('Listing URLs...')
    for i in range(len(df_game_summaries)):
        urls.append(f'https://steamspy.com/api.php?request=appdetails&appid={list_of_appids[i]}')
    print('----------------\nDone Listing.\n\n')
    
    print('Loading JSON Request')
    with Pool(10) as pool:
        jsons = pool.map(get_data, [url for url in urls[:12500]]) # next: 12501 - 25000
    print('----------------\nLoading successful!\n\n')
    
    print('Saving to JSON file...')
    with open('datasets/steam_dataset/json/steamapi_games.json', 'w+') as file:
        json.dump([js.__dict__ for js in jsons], file, indent=1)
    print('----------------\nSaved ssuccessfully!')