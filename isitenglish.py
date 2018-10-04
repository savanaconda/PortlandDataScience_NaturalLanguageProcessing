# This python script looks a board game review comments and attempts to determine
# if the comments are english or not. To do this, it scraps the 100 most common words
# in English from a wikipedia page, then breaks the board game comments into individual words.
# If a comment contains one of the 100 most common words, it is deemed English.
#
# This algorithm is somewhat limiting as it fails if any of the 100 most common words
# in English happen to exist in another language. Also, this algorithm fails if the comment is
# too short (a common challenge). The code will warn the user that a comment is too short (less
# than 4 words) to process.
#
# Further, I loaded Google's public port of one of their language detection algorithms
# to compare my results to their results. This algorithm had a similar challenge with
# short comments as well
#
# Results are printed in 4 csv files: english comments and non-english comments (my
# algorithm) and google english comments and google non-english comments

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import nltk
import numpy as np
from langdetect import detect
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
ps = PorterStemmer()

#Decide whether or not to use stemming on comments before processing
stem_please = 1


### Gets the 100 most common words in the English language from Wikipedia ###
def scrap_most_common_words():
	WIKI_URL = "https://en.wikipedia.org/wiki/Most_common_words_in_English"

	req = requests.get(WIKI_URL)
	soup = BeautifulSoup(req.content, 'lxml')
	table_classes = {"class": ["sortable", "plainrowheaders"]}
	wikitables = soup.findAll("table", table_classes)
	mytable = wikitables[0]

	common_words_list = []

	table = soup.find('span', id='100_most_common_words').parent.find_next_sibling('table')
	for single in table.find_all('td'):
		words = single.find_all(re.compile('[a-z]+'))
		for elem in words:
			# only lowercase words (remove titles)
			if elem.text.lower() == elem.text:
				common_words_list.append(elem.text)

	return common_words_list

most_common = scrap_most_common_words()
# print(most_common)
#############################################################################




### Read in data ###
data = pd.read_csv('boardgame-frequent-user-comments.csv', encoding = "utf-8",  skiprows=[2678])
####################



### Testing Chinese as ??? issue ###
test = data.iloc[494]
# test.to_csv('chin.csv')
####################################



all_comments = data['comment']
comments = all_comments[0:1000]   # Only getting the first 1000 to make things faster
eng = []
allcoms_rate = []
google_answers = []
enough_words = []



### For each comment, get what language the google-based language detection library identifies it as ###
for com in comments:
	try:
		google_answers.append(detect(com))
	except Exception as ex:
		google_answers.append('ERROR ON THE DANCE FLOOR')
########################################################################################################	
	


### For each comment, check if any of the words in that comment are on the 100 most common English words list ###
for com in comments:

	# Create tokens -- ensure that it is words only (not punctuation)
	tokens = nltk.word_tokenize(com)
	tokenizer = RegexpTokenizer(r'\w+')
	words_only = tokenizer.tokenize(com)

	# Add stemming
	if stem_please == 1:
		stems = []
		for word in words_only:
			stems.append(ps.stem(word))
		words_only = stems

	# Check if comment is too short (it will often fail algorithm if it is)
	if len(words_only) < 4:
		enough_words.append("TOO SHORT")
	else:
		enough_words.append("ok")

	# Loop each word in 100 most common list, rate 0 or 1 if word match, then OR operation to see if there are any matches
	com_rate = []
	for word in most_common:
		for token in words_only:
			lower_token = token.lower()
			if lower_token == word:
				com_rate.append(1)
			else:
				com_rate.append(0)
	allcoms_rate.append(np.any(com_rate))
#################################################################################################################



### Compile answers from google algorithm ###
google_answers_df = pd.Series(google_answers)
enough_words_df = pd.Series(enough_words)
answers = pd.concat([comments, google_answers_df.rename('language'), enough_words_df.rename('enough words')], axis=1)
google_eng_comments = answers[answers['language']=='en']
google_noteng_comments = answers[answers['language']!='en']

# print(google_eng_comments.head(50))
# print(google_noteng_comments.head(50))
#############################################


### Compile answers from my algorithm ###
rates = pd.Series(allcoms_rate)
combo = pd.concat([comments,rates.rename('eng')], axis=1)
eng_comments = combo[combo['eng']==1]
noteng_comments = combo[combo['eng']==0]
#########################################


### Write results to CSV file ###
noteng_comments.to_csv('non_english_comments.csv')
eng_comments.to_csv('english_comments.csv')
google_noteng_comments.to_csv('google_non_english_comments.csv')
google_eng_comments.to_csv('google_english_comments.csv')
#################################














# for line in mytable.findall('<tr><a class='):
# 	pritn(line.name)



# >the</a></td>