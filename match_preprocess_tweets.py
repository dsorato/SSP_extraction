import os
import json
import re
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.dicts.emoticons import emoticons
from nltk.stem import WordNetLemmatizer
from gensim.models import KeyedVectors

from dynamic_context_window import * 
from ssp_extraction import *
from application_context import *

tknzr = TweetTokenizer()
lemmatizer = WordNetLemmatizer()
matched_docs = [] 

text_processor = TextPreProcessor(
    fix_html=True,  # fix HTML tokens
    segmenter="twitter", 
    corrector="twitter", 
    
    unpack_hashtags=True,  # perform word segmentation on hashtags
    unpack_contractions=True,  # Unpack contractions (can't -> can not)
    spell_correct_elong=True,  # spell correction for elongated words
    
    #tokenizer=SocialTokenizer(lowercase=True).tokenize,
    
    dicts=[emoticons]
)

######## PREPROCESSING ##############
def remove_usermention_URL_RT(input_sentence):
	input_sentence = re.sub(r"http\S+", "", input_sentence)
	input_sentence = re.sub("RT", "", input_sentence)
	input_sentence = re.sub(r"@[^\s]+", "", input_sentence)


	return input_sentence

# def transform_contractions(input_sentence):
# 	input_sentence = contractions.fix(input_sentence)

# 	return input_sentence

def remove_punctuation(input_sentence):
	input_sentence = re.sub(r"[^\w\d'\s]+",'',input_sentence)

	return input_sentence

def remove_whitespaces(input_sentence):
	input_sentence = input_sentence.strip('\t')
	input_sentence = input_sentence.strip('\n')
	input_sentence = input_sentence.strip()
	input_sentence = input_sentence.replace('\n','')
	input_sentence = input_sentence.replace('\t','')
	
	return input_sentence

def ekphrasis_preprocessing(input_sentence):

	return "".join(text_processor.pre_process_doc(input_sentence))

def tokenize(input_sentence):

	return tknzr.tokenize(input_sentence)

#Lemmatize a list of tokenized words
def lemmatize(tokens):
    lemmas = []
    for token in tokens:
        lemma = lemmatizer.lemmatize(token)
        lemmas.append(lemma)
    return lemmas

#########################################

#lowecase a list of lemmatized words
def lowercase(tokens):
    lowercased = []
    for token in tokens:
        lower = token.lower()
        lowercased.append(lower)

    return lowercased

#########################################


######## Match docs with keywords ############# 

def get_docs_with_keywords(key, doc, keyword_list):
	intersection = set(keyword_list) & set(doc)
	if len(intersection) == 1:
		index = doc.index(next(iter(intersection)))
		context_window = ContextWindow(key, doc, index)
		matched_docs.append(context_window)
	if len(intersection) > 1:
		for item in intersection:
			index = doc.index(item)
			context_window = ContextWindow(key, doc, index)
			matched_docs.append(context_window)

#########################################



def print_dict(dictionary):
	for k,v in list(dictionary.items()):
		print(k,v)


def main():
	currdir = os.getcwd()

	application = None
	if ApplicationContextFactory().can_load_appctx():
		print('loading...')
		application = ApplicationContextFactory().load()
	else:
		application = ApplicationContext()

	keyword_list = ['sexist', 'bitch', 'whore', 'stupid']
	
	# #insert here your dataset if you wanna train a word embedding model
	# data = []
	# with open('data/dataset') as csvfile:
	# 	reader = csv.DictReader(csvfile)
	# 	for row in reader:
	# 		data.append(row['tweet'])
	# csvfile.close()

	# # #Train a model or...
	# # train_model = TrainModel(clean_stop_word_list)
	# # if train_model.check_can_load():
	# # 	print('loading model...')
	# # 	model = FastText.load(currdir+'/mymodel.bin')
	# # else:
	# # 	model = train_model.train()
	# # word_vectors = model.wv

	#...load pre trained model
	word_vectors = KeyedVectors.load_word2vec_format(("data/glove_to_word2vec_twitter.bin"), binary=True)

	#insert here your dataset to extract SSP (example for tweets in a json file)
	data_to_analyze = {}
	with open('data/sexism.json') as tweet_data:
		for line in tweet_data:
			tweet = json.loads(line)
			tweet_id = tweet.get('id')
			if tweet.get('retweeted_status'):
				tweet_text = tweet['retweeted_status'].get('text')
			else:
				tweet_text = tweet['text']
				data_to_analyze[tweet_id] = tweet_text
	tweet_data.close()

	# data_to_analyze[1] = "@someone I swear, I'm #notsexist, but I honestly just cannot stand the woman college football announcer on ESPN2"
	# data_to_analyze[2] = "I am sorry I am not sexist but that is why girls should not ref boys games."



	preprocessed = {}
	for k, v in list(data_to_analyze.items()):
		v = remove_usermention_URL_RT(v)
		v = ekphrasis_preprocessing(v)
		v = remove_punctuation(v)
		v = remove_whitespaces(v)
		v = tokenize(v)
		v = lemmatize(v)
		v = lowercase(v)
		preprocessed[k] = v

	#print_dict(preprocessed)
	for k,v in list(preprocessed.items()):
		get_docs_with_keywords(k, v, keyword_list)

	application.update_matched_docs(matched_docs)
	# for item in application.matched_docs:
	# 	item.print_cw()
	
	expand_context(application, word_vectors)



if __name__ == "__main__":
	main()
