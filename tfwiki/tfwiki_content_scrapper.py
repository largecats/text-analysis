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
import tfwiki_url_scrapper

CSV_PATH = 'C:\\Users\\xiaolinfan\\Fun\\programming\\personal-projects\\text-analysis\\tfwiki\\content.csv'

def read_from_csv(csvPath):
    df = pd.read_csv(csvPath, encoding='ANSI') # see comments in accepted answer https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
    return df

def get_content(url):
    pageHtml = tfwiki_url_scrapper.get_page_html(url)
    content = pageHtml.find('div', attrs={'id':'mw-content-text','class':'mw-content-ltr'}).text
    content = content.replace('\n', '').replace('\t', '')
    return content

def get_all_content(df, csvPath, startFrom):
    results = []
    for i in range(len(df.index)):
        if i >= startFrom:
            print('i={}'.format(i))
            sleep(random.uniform(2, 5))
            title = df['name'][i]
            url = df['url'][i]
            content = get_content(url)
            print('title={}, url={}\n content={}'.format(title, url, content[:100]))
            results.append({'title':title, 'url':url, 'content':content})
            if not os.path.exists(os.path.dirname(csvPath)):
                os.makedirs(os.path.dirname(csvPath))
            with open(csvPath, 'a', encoding='utf-8', newline='') as output:
                writer = csv.writer(output)
                if i == 0:
                    writer.writerow(['title', 'url', 'content'])
                writer.writerow([title, url, content])
    return results

if __name__ == '__main__':
    df = read_from_csv(tfwiki_url_scrapper.CSV_PATH)
    results = get_all_content(df, CSV_PATH, 0)
    # tfwiki_url_scrapper.write_dict_to_csv(results, CSV_PATH)
