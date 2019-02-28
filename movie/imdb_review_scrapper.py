#https://www.dataquest.io/blog/web-scraping-beautifulsoup/

import requests
from lxml import html
import re
import pandas as pd
import numpy as np
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

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

# Do not load images
options=webdriver.ChromeOptions()  
prefs={  
     'profile.default_content_setting_values': {  
        'images': 2 
    }  
}  
options.add_experimental_option('prefs',prefs)  
  
browser = webdriver.Chrome(chromedriver, chrome_options=options)
browser.set_page_load_timeout(30)

# G1
url = 'https://www.imdb.com/title/tt0086817/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# G1 The Movie
# url = 'https://www.imdb.com/title/tt0092106/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF1
# url = 'https://www.imdb.com/title/tt0418279/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF2
# url = 'https://www.imdb.com/title/tt1055369/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF3
# url = 'https://www.imdb.com/title/tt1399103/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF4
# url = 'https://www.imdb.com/title/tt2109248/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF5
# url = 'https://www.imdb.com/title/tt3371366/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0'
# BBB
# url = 'https://www.imdb.com/title/tt4701182/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0' # Without spoilers
browser.get(url)
print(browser.title)

# Dedeclaring the lists to store data in
titles = []
ratings = []
comments = []

# Click "load more" to load all results until there is no more "load more" button
while True:
    try:
        loadMoreButton = browser.find_element_by_class_name('ipl-load-more__button')
        loadMoreButton.click()
        time.sleep(2) # wait for the next load more button to load
    except:
        break

reviews = browser.find_elements_by_class_name('review-container')
for review in reviews:
    html = review.get_attribute('innerHTML')
    try:
        rating = re.findall(r'<span>(\d{1,2})</span>', html)[0]
    except:
        rating = ''
    title = re.findall(r'class="title">(.*?)\n</a>', html)[0]
    try:
        comment = re.findall(r'<div class="text show-more__control">(.*?)</div>', html, re.DOTALL)[0]
    except:
        comment = re.findall(r'<div class="text show-more__control clickable">(.*?)</div>', html, re.DOTALL)[0]
    comment = re.sub("<br><br>", " ", comment)
    comment = re.sub("\n", " ", comment)
    # comment = re.sub("&amp;", "&", comment)
    print(comment)
    ratings.append(rating)
    titles.append(title)
    comments.append(comment)

movieReviews = pd.DataFrame({'rating': ratings, 'title': titles, 'review': comments}, columns = ['rating', 'title', 'review'])
fileName = "C:\\Users\\LinFan Xiao\\Fun\\Programming\\For fun\\web scraping\\TF movie review\\reviews.csv"
movieReviews.to_csv(fileName, sep=",", encoding = "utf-8", index=False)