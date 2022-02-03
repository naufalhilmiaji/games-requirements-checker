import pandas as pd
import numpy as np
import requests, json, re, time, os

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ua = UserAgent()
options = Options()
options.add_argument('headless')
driver = webdriver.Chrome("C:/Users/cilac/OneDrive/Documents/chromedriver.exe", options=options)
driver.set_page_load_timeout(15)

def get_appid_lists():
    df = pd.read_csv('datasets/steam_dataset/steamapi/csv/game_details.csv', sep=',').reset_index()
    df.drop('Unnamed: 0', axis=1, inplace=True)
    dropdup = df[~df['appid'].duplicated()]
    result = list(dropdup['appid'])

    return result

def get_url(appid):

    return f'https://store.steampowered.com/api/appdetails?appids={appid}'

def get_api(url):
    finished = 0
    while finished == 0:
        try:
            driver.get(url)
            soup = bs(driver.page_source)
            finished = 1
            if soup:
                jsons = json.loads(soup.find("body").text)
                return jsons
            else:
                return 'Not Found'
        except Exception as e:
            time.sleep(10)
            print(f'--- ERROR -> get_api: {e}')

if __name__ == '__main__':
    start_time = time.time()
    print('----------\nGetting APPIDs...')
    appids = get_appid_lists()
    print('APPIDs ready!\n----------\n')
    
    print('----------\nRequesting API...')
    json_object = []
    for appid in appids[30000:40000]:
        print(f'Requesting API -> APPID: {appid}...')
        url = get_url(appid)
        json_object.append(get_api(url))
        time.sleep(1)
        os.system('cls')
    print('API requests completed!\n----------')
    print(f'--- Program Runtime: {(time.time() - start_time)//60} minutes ---\n\n')

    print('----------\nSaving to JSON file...')
    path = 'datasets/steam_dataset/steamapi/json/ss_details.json'
    
    if not os.path.isfile(path):
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(json_object, file, indent=5, ensure_ascii=False)
    else:
        with open(path, 'r', encoding='UTF-8') as file:
            ss_details = json.load(file)

        ss_details.append(json_object)
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(ss_details, file, indent=5, ensure_ascii=False)
    print('Saved successfully!\n----------')