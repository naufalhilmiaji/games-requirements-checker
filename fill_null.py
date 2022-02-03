import pandas as pd
import numpy as np
import requests, json, re, time, os

from collections import defaultdict
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

df = pd.read_csv('D:\Projects\Github\games-requirements-checker\datasets\steam_dataset\steamapi\csv\game_details.csv', sep=',')
options = Options()
options.add_argument('headless')
driver = webdriver.Chrome("C:/Users/cilac/OneDrive/Documents/chromedriver.exe", options=options)

path = 'D:\Projects\Github\games-requirements-checker\datasets\steam_dataset\steamapi\json\ss_details.json'
with open(path, 'r', encoding='UTF-8') as file:
    data = json.load(file)

def get_url(appid):

    return f'https://store.steampowered.com/api/appdetails?appids={appid}'

def get_api(url):
    try:
        driver.get(url)
        soup = bs(driver.page_source, 'lxml')

        if soup:
            jsons = json.loads(soup.find("body").text)
            return jsons
        else:
            return 'Not Found'
    except Exception as e:
        print(f'--- ERROR -> get_api: {e} -> {url}')

# def fill(df, data):
#     empties = [i for i,x in enumerate(data) if not x]
#     if len(empties) > 0:
#         for idx in empties:
#             appid = df['appid'][idx]
#             api = get_api(get_url(appid))
#             data[idx] = api
#         fill(df, data)
#     return data
empties = [i for i,x in enumerate(data) if not x]
for idx in empties:
    appid = df['appid'][idx]
    api = get_api(get_url(appid))
    data[idx] = api
empties = [i for i,x in enumerate(data) if not x]
len(empties)

with open(path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=5, ensure_ascii=False)