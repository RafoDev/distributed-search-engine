from pymongo import MongoClient
from .porterStemmer import PorterStemmer
from django.http import JsonResponse
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('stopwords')


def preproccess(data):
    stemmer  = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    prepro_data = []

    prepro_words = [stemmer.stem(word) for word in data if word not in stop_words]
    prepro_data.append(' '.join(prepro_words))
    print(''.join(prepro_data))
    return ''.join(prepro_data)


client = MongoClient('localhost', 27017)
db = client['search_engine_db']

collection_ii = db['inverted_index']
collection_pr = db['page_rank']
collection_meta = db['metadata']


# def get_docs_by_word(word):
#     document = collection_ii.find_one({"word": word})
#     if document:
#         docs = []
#         for post in document['postings']:
#             docs.append(post["file"])
#         return docs
#     else:
#         return None

def get_docs_by_word(word):

    query = {"$text": {"$search": word}}
    documents = collection_ii.find(query)

    docs = []
    for document in documents:
        for post in document.get('postings', []):
            docs.append(post.get("file"))

    return docs if docs else None

def get_document_by_pid(pid):
    document = collection_meta.find_one({'pid': pid})
    if document and '_id' in document:
        del document['_id']
    return document


def get_rank_by_doc(filename):
    document = collection_pr.find_one({"filename": filename})
    if document:
        return document['rank']
    else:
        return None


porter = PorterStemmer()


def search_query(value):

    prepro_value = preproccess(value)

    words = []

    for word in prepro_value:
        words.append(word)
        # word = porter.stem(word, 0, len(word)-1)

    if len(prepro_value):
        result = []
        i = 0
        for word in prepro_value:
            word_is_in_ii = get_docs_by_word(word)
            if word_is_in_ii:
                result.append([word_is_in_ii, words[i]])
                i += 1
        return result

    return []
