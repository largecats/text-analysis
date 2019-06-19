##################################################
#                 import modules                 #
##################################################
import os
import nltk
import csv
import pandas as pd
import re
import random
import matplotlib.pyplot as plt
import numpy as np

##################################################
#                    read csv                    #
##################################################
# set working directory
path = ""
os.chdir(path)

fileName = "reviews.csv"
df = pd.read_csv(fileName)
print(df.head(5))

##################################################
#                   word cloud                   #
##################################################
# tokenize into words
from nltk.tokenize import word_tokenize
tokenizedWords = []
for i in range(len(df.index)):
    review = df['title'][i]
    # or use full review
    # review = df['review'][i]
    tokenizedWord = word_tokenize(review)
    tokenizedWords.append(tokenizedWord)

# remove stop words and punctuations
from nltk.corpus import stopwords
punctuations = ['.', ',', ';', ':', '!', '?']
stopWords = set(stopwords.words("english"))
filteredtokenizedWords = []
for tokenizedWord in tokenizedWords:
    filteredtokenizedWord = []
    for word in tokenizedWord:
        if (word not in stopWords) and (word not in punctuations):
            filteredtokenizedWord.append(word)
    filteredtokenizedWords.append(filteredtokenizedWord)

# merge list of lists into one list
words = []
for filteredtokenizedWord in filteredtokenizedWords:
    for word in filteredtokenizedWord:
        words.append(word)

# pos Tagging
tags = nltk.pos_tag(words)

# lemmatization
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
lemWords = []
for i in range(len(words)):
    word = words[i]
    tag = tags[i][1]
    if tag == 'VB' or tag == 'VBP':
        lemWord = lem.lemmatize(word, "v")
    elif tag == "PRP":
        lemWord = word
    else:
        lemWord = lem.lemmatize(word)
    lemWords.append(lemWord.lower())

# remove uninformative words
filteredWords = []
for lemWord in lemWords:
    if lemWord not in ["movie", "film", "review", "spoiler", "transformer", "transformers", "n't", "age", "extinction", "dark", "moon", "last", "knight", "revenge", "fallen", "one", "episode", "series", "show", "season"]:
        filteredWords.append(lemWord)

# merge list of words into one string
text = ' '.join(filteredWords)

# create word cloud
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def grey_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
# mask
mask = np.array(Image.open("BBB_poster.jpg"))
# generate word cloud image
wordcloud = WordCloud(mask = mask).generate(text)
# diplay image
plt.figure(figsize=(18,12))
plt.imshow(wordcloud.recolor(color_func = grey_color_func, random_state = 3), interpolation = 'bilinear')
plt.axis("off")
plt.savefig("review_wordcloud.png", format = "png")
plt.show()

##################################################
#               sentiment analysis               #
##################################################
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
nltk.download('vader_lexicon')

# tokenize into sentences
tokenizedSents = []
for i in range(len(df.index)):
    review = df['title'][i]
    # or use full review
    # review = df['review'][i]
    tokenizedSent = sent_tokenize(review)
    tokenizedSents.append(tokenizedSent)

# merge list of lists into one list
sents = []
for tokenizedSent in tokenizedSents:
    for sent in tokenizedSent:
        sents.append(sent)

# polarity scores
neg = []
neu = []
pos = []
compound = []
sia = SentimentIntensityAnalyzer()
for sent in sents:
    print(sent)
    ps = sia.polarity_scores(sent)
    print(ps)
    neg.append(ps["neg"])
    neu.append(ps["neu"])
    pos.append(ps["pos"])
    compound.append(ps["compound"])
scores = pd.DataFrame({'negative': neg, 'neutral': neu, 'positive': pos, 'compound': compound}, columns = ['negative', 'neutral', 'positive', 'compound'])
print(scores.info())
print(scores.head(10))

# visualization
plt.hist(scores['compound'])
plt.title("Movie review polarity scores")
plt.savefig("review_polarity_scores.png")
plt.show()