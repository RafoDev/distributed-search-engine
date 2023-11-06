from pymongo import MongoClient
from .porterStemmer import PorterStemmer

client = MongoClient('localhost', 27017)
db = client['search_engine_db']

collection_ii = db['inverted_index']
collection_pr = db['page_rank']

def get_docs_by_word(word):
    document = collection_ii.find_one({"word": word})
    if document:
        docs = []
        for post in document['postings']:
            docs.append(post["file"])
        return docs
    else:
        return None

def get_rank_by_doc(filename):
    document = collection_pr.find_one({"filename": filename})
    if document:
        return document['rank']
    else:
        return None


porter=PorterStemmer()

def search_query(value):

	words = []

	for word in value:
		words.append(word)
		word =	porter.stem(word, 0, len(word)-1)

	if len(value):
		result = []
		i = 0
		for word in value:
			word_is_in_ii = collection_ii.find_one({"word": word})
			if word_is_in_ii:
				result.append([get_docs_by_word(word), words[i]])
				i += 1
		return result

	return []			