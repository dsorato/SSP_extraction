from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models import FastText
import os

class TrainModel(object):
	def __init__(self, sentences):
		self.sentences = sentences

	def train(self):
		model = FastText(self.sentences, size=200, window=3, min_count=1, iter=70)
		currdir = os.getcwd()
		model.save(currdir+'/mymodel.bin')
		return model

	def check_can_load(self):
		return os.path.isfile('mymodel.bin')