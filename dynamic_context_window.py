class ContextWindow(object):
	def __init__(self, tweet_id, sentence, keyword_index):
		self.tweet_id = tweet_id
		self.sentence = sentence
		self.keyword_index = keyword_index
		self.ssp_instance = []
		self.right_border = None
		self.left_border = None
		self.can_expand_right = True
		self.can_expand_left = True
		self.can_expand = True

	def print_cw(self):
		print(self.tweet_id, self.sentence, self.keyword_index)


	#check if instance still can expand to the left side
	def instance_can_expand_left_border(self):
		if self.left_border<=0:
			self.can_expand_left = False
			if self.can_expand_right == False and self.can_expand_left == False:
				self.can_expand=False

		return self.can_expand_left

	#check if instance still can expand to the right side
	def instance_can_expand_right_border(self):
		if self.right_border>=len(self.sentence):
			self.can_expand_right = False
			if self.can_expand_right == False and self.can_expand_left == False:
				self.can_expand=False

		return self.can_expand_right


	#expand instance, if possible
	def try_to_expand(self):
		#if the phrase has only one word, it is the ssp instance and it can't be expanded
		if len(self.sentence) == 1:
			self.ssp_instance = self.sentence
			self.can_expand_right = False
			self.can_expand_left = False
			self.can_expand = False

		else:
			if self.right_border == None or self.left_border == None:
				self.right_border = self.keyword_index+1
				self.left_border = self.keyword_index-1
				self.ssp_instance = self.sentence[self.left_border:self.right_border]
			else:
				if self.instance_can_expand_left_border() and self.instance_can_expand_right_border():
					self.right_border = self.right_border+1
					self.left_border = self.left_border-1
					self.ssp_instance = self.sentence[self.left_border:self.right_border]
				elif self.instance_can_expand_left_border() == False and self.instance_can_expand_right_border() == True:
					self.right_border = self.right_border+1
					self.ssp_instance = self.sentence[self.left_border:self.right_border]
				elif self.instance_can_expand_left_border() == True and self.instance_can_expand_right_border() == False:
					self.left_border = self.left_border-1
					self.ssp_instance = self.sentence[self.left_border:self.right_border]


		return self.ssp_instance


	def print_ssp_instance(self):
		print(self.ssp_instance)