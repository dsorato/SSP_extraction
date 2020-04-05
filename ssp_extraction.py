from application_context import *

def eliminate_words(element, word_vectors):
	clean = list(filter(lambda x: x in word_vectors.vocab, element))
	print('clean', clean)

	return clean


def expand_context(application, word_vectors):
	for i, element in enumerate(application.matched_docs[application.list_index:]):
		doc_1 = application.matched_docs[i]
		for j, element in enumerate(application.matched_docs[application.list_index+1:]):
			doc_2 = application.matched_docs[j]
			if doc_1.tweet_id != doc_2.tweet_id:
				sim = word_vectors.n_similarity(doc_1.sentence[doc_1.keyword_index], doc_2.sentence[doc_2.keyword_index])
				print(doc_1.sentence[doc_1.keyword_index], doc_2.sentence[doc_2.keyword_index], sim)
				while (doc_1.can_expand==True and doc_2.can_expand==True) and sim >= 0.86:
					doc_1.try_to_expand()
					doc_2.try_to_expand()
					sim = word_vectors.n_similarity(eliminate_words(doc_1.ssp_instance, word_vectors), eliminate_words(doc_2.ssp_instance, word_vectors))
					doc_1.print_ssp_instance()
					doc_2.print_ssp_instance()
					print(sim)

		if doc_1.ssp_instance is not None and len(doc_1.ssp_instance)>=3 and doc_2.ssp_instance is not None and len(doc_2.ssp_instance) >=3:
				application.instance.ssp_instances.append(doc_1.ssp_instance)
				application.instance.ssp_instances.append(doc_2.ssp_instance)

		application.instance.list_index += 1
		if application.instance.list_index%20 == 0:
			ApplicationContextFactory().save()

	ApplicationContextFactory().save()

	for item in application.instance.ssp_instances:
		print(item)
