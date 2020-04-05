import os.path

import pickle

class ApplicationContext:
	instance = None

	def __init__(self):
		self.list_index = 0
		self.matched_docs = []
		self.ssp_instances = []
		ApplicationContext.instance = self

	def update_matched_docs(self, matched_docs):
		self.matched_docs = matched_docs

class ApplicationContextFactory:
	filename_ssp = 'patterns.dat'

	def save(self):
		with open(ApplicationContextFactory.filename_ssp, 'wb') as file:
			pickle.dump(ApplicationContext.instance, file)

	def load(self):
		with open(ApplicationContextFactory.filename_ssp, 'rb') as file:
			ApplicationContext.instance = pickle.load(file)
			return ApplicationContext.instance

	#Check if file exists 
	def can_load_appctx(self):
		return os.path.isfile('patterns.dat')
