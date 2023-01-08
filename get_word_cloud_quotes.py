from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')
from os import listdir, path
from collections import namedtuple
import argparse
import re
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

quotes_list = []
cue_list = []
entity_list = []
with open("./output4.txt", 'r') as fi:
            for line in fi:
                words = re.split(r' ', line)
                if len(words) > 0:
                    # print(words[-1])
                    if "Quotation" in words[-1]:
                        quotes_list.append(words[0])
                    if "Cue" in words[-1]:
                        cue_list.append(words[0])
                    if "Entity" in words[-1]:
                        entity_list.append(words[0])       

print(len(quotes_list))
print(len(cue_list))
print(len(entity_list))


text = ""
print(quotes_list[:24])
for i in quotes_list:
    if i == "[CLS]" or i == "[SEP]" or "#" in i or i == 's':
        continue
    else:
        text+=" "+i
wordcloud = WordCloud(background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

text = ""
print(cue_list[:24])
for i in cue_list:
    if i == "[CLS]" or i == "[SEP]" or "#" in i or i == 's':
        continue
    else:
        text+=" "+i
wordcloud = WordCloud(background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

text = ""
print(entity_list[:24])
for i in entity_list:
    if i == "[CLS]" or i == "[SEP]" or "#" in i or i == 's':
        continue
    else:
        text+=" "+i
wordcloud = WordCloud(background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

