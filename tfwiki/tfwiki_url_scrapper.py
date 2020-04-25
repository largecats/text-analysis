import requests
import re
import numpy as np
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
#import urllib
from IPython.core.display import clear_output
from time import sleep
from random import randint
from warnings import warn
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv

URL = 'https://tfwiki.net/mediawiki/index.php?title=Special%3AAllPages&from=&to=&namespace=0'
CSV_PATH = 'C:\\Users\\xiaolinfan\\Fun\\programming\\personal-projects\\text-analysis\\tfwiki\\urls.csv'

def write_dict_to_csv(d, csvPath):
    pd.DataFrame(d).to_csv(csvPath, index=False, encoding='utf-8')

def convert_to_url(url):
    if not url.startswith('http'):
        url = 'https://tfwiki.net' + url
    return url

def get_page_html(url):
    sleep(random.uniform(0.5, 2))
    response = requests.get(url)
    pageHtml = BeautifulSoup(response.text, 'html.parser')
    return pageHtml

def get_urls(pageHtml):
    allPagesList = pageHtml.find('table', class_='allpageslist')
    if allPagesList is None:
        allPagesTableChunk = pageHtml.find('table', class_='mw-allpages-table-chunk')
        if allPagesTableChunk is None:
            return None
        else:
            results = []
            urlInfos = allPagesTableChunk.find_all('td')
            for urlInfo in urlInfos:
                url, pageName = urlInfo.a.get('href'), urlInfo.a.get('title')
                url = convert_to_url(url)
                print('name={}, url={}'.format(pageName, url))
                results.append({'name':pageName, 'url':url})
            return results
    else:
        results = []
        urlFromTos = allPagesList.find_all('tr')
        for urlFromTo in urlFromTos:
            url = convert_to_url(urlFromTo.find('td', class_='mw-allpages-alphaindexline').a.get('href'))
            urls = get_urls(get_page_html(url))
            if urls:
                results += urls
            else:
                pattern = re.compile(r'(.+) to .+', flags=re.DOTALL)
                pageName = pattern.findall(urlFromTo.text)[0]
                print('name={}, url={}'.format(pageName, url))
                results.append({'name':pageName, 'url':url})
        return results

if __name__ == '__main__':
    pageHtml = get_page_html(URL)
    urls = get_urls(pageHtml)
    write_dict_to_csv(d=urls, csvPath=CSV_PATH)
