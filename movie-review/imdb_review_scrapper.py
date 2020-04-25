##################################################
#                 import modules                 #
##################################################
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

##################################################
#                 set up browser                 #
##################################################
chromedriver = "path-to\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

# do not load images
options = webdriver.ChromeOptions()  
prefs = {  
     'profile.default_content_setting_values': {  
        'images': 2 
    }  
}  
options.add_experimental_option('prefs',prefs)  

browser = webdriver.Chrome(chromedriver, chrome_options = options)
browser.set_page_load_timeout(60)

##################################################
#                   main work                    #
##################################################
# set working directory
path = ""
os.chdir(path)

# movie reviews
# G1 series
# url = 'https://www.imdb.com/title/tt0086817/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# G1 The Movie
# url = 'https://www.imdb.com/title/tt0092106/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF1
# url = 'https://www.imdb.com/title/tt0418279/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF2
# url = 'https://www.imdb.com/title/tt1055369/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF3
# url = 'https://www.imdb.com/title/tt1399103/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF4
# url = 'https://www.imdb.com/title/tt2109248/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# TF5
# url = 'https://www.imdb.com/title/tt3371366/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'
# BBB
url = 'https://www.imdb.com/title/tt4701182/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0'

browser.get(url)
print(browser.title)

# declare empty lists to store data in
titles = []
ratings = []
comments = []

# click "load more" to load all results until there is no more "load more" button
while True:
    try:
        loadMoreButton = browser.find_element_by_class_name('ipl-load-more__button')
        loadMoreButton.click()
        # wait for the next load more button to load; note that if the wait is too short, the next load button may not be clicked
        time.sleep(10) 
    except:
        break

reviews = browser.find_elements_by_class_name('review-container')
print(len(reviews))
for review in reviews:
    html = review.get_attribute('innerHTML')
    # extract rating if available
    try:
        rating = re.findall(r'<span>(\d{1,2})</span>', html)[0]
    except:
        rating = ''
    title = re.findall(r'class="title">(.*?)\n</a>', html)[0]
    # click show more if available
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
print(movieReviews.info())
print(movieReviews.head(10))
fileName = "reviews.csv"
movieReviews.to_csv(fileName, sep = ",", encoding = "utf-8", index = False)