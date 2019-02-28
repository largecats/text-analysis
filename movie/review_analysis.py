# https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
# https://amueller.github.io/word_cloud/auto_examples/a_new_hope.html#

import nltk
import csv
import pandas as pd
import re
# nltk.download()

fileName = "C:\\Users\\LinFan Xiao\\Fun\\Programming\\For fun\\web scraping\\TF movie review\\reviews.csv"
df = pd.read_csv(fileName)
print(df.head(5))

# Tokenization
from nltk.tokenize import word_tokenize
tokenizedReviews = []
for i in range(len(df.index)):
    review = df['review'][i]
    tokenizedReview = word_tokenize(review)
    tokenizedReviews.append(tokenizedReview)

# Removing stop words and punctuations
punctuations = ['.', ',', ';', ':', '!', '?']
from nltk.corpus import stopwords
stopWords = set(stopwords.words("english"))
filteredTokenizedReviews = []
for tokenizedReview in tokenizedReviews:
    filteredTokenizedReview = []
    for word in tokenizedReview:
        if (word not in stopWords) and (word not in punctuations):
            filteredTokenizedReview.append(word)
    filteredTokenizedReviews.append(filteredTokenizedReview)

# Merge list of lists into one list
words = []
for filteredTokenizedReview in filteredTokenizedReviews:
    for word in filteredTokenizedReview:
        words.append(word)

# POS Tagging
tags = nltk.pos_tag(words)

# Lemmatization
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
    lemWords.append(lemWord)

# Remove uninformative words
filteredWords = []
for lemWord in lemWords:
    if lemWord not in ["movie", "film", "Transformer", "Transformers", "transformer", "transformers", "n't"]:
        filteredWords.append(lemWord)

# Merge list of words into one string
text = ' '.join(filteredWords)

# Create word cloud
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
# Mask
mask = np.array(Image.open("C:\\Users\\LinFan Xiao\\Fun\\Programming\\For fun\\web scraping\\TF movie review\\BBB_poster.jpg"))
# Create and generate a word cloud image
wordcloud = WordCloud(mask = mask).generate(text)
# Display the generated image
plt.figure(figsize=(18,12))
plt.imshow(wordcloud.recolor(color_func = grey_color_func, random_state=3), interpolation='bilinear')
# plt.imshow(wordcloud.recolor(color_func = ImageColorGenerator(mask)), interpolation='bilinear')
# plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("C:\\Users\\LinFan Xiao\\Fun\\Programming\\For fun\\web scraping\\TF movie review\\review_wordcloud.png", format="png")
plt.show()

# from nltk.probability import FreqDist
# fdist = FreqDist(filteredWords)
# fdist.plot(30,cumulative=False)
# plt.show()