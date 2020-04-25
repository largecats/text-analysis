##################################################
#                 import modules                 #
##################################################
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import os
import random
import nltk

##################################################
#                   read file                    #
##################################################
# set working directory
path = "<working_directory>"
os.chdir(path)

fileName = input("Please enter text file name: ")
with open(fileName, 'r') as file:
    text = file.read().replace('\n', ' ')

print(text)

##################################################
#                text processing                 #
##################################################
# turn to lowercase
text = text.lower()

# define words that are to be ignored in the word cloud
stopwords = set(STOPWORDS)
# stopwords.update(["project", 'use', 'hospital', 'bi', 'diagnosis'])

# tokenize into words
from nltk.tokenize import word_tokenize
words = word_tokenize(text)

# pos tagging
tags = nltk.pos_tag(words)

# lemmatization
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
lemWords = []
for i in range(len(words)):
    word = words[i]
    tag = tags[i][1]
    if 'VB' in tag:
        lemWord = lem.lemmatize(word, "v")
    elif tag == "PRP":
        lemWord = word
    else:
        lemWord = lem.lemmatize(word)
    lemWords.append(lemWord)

finalText = ' '.join(lemWords)

##################################################
#               create word cloud                #
##################################################
# linkedin background photo size is 1564x396
wordcloud = WordCloud(width = 1584, height = 396, 
                background_color ='black',
                min_font_size = 5,
                stopwords = stopwords,
                random_state = 42).generate(finalText) 

# a grey scale color function
def grey_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# plot the wordcloud image
plt.figure(figsize = (8, 2), facecolor = None) 
plt.imshow(wordcloud)
plt.imshow(wordcloud.recolor(color_func = grey_color_func, random_state = 3), interpolation = "bilinear")
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.savefig("wordcloud.png")
plt.show()