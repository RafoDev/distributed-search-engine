from config import db

collection_ii = db['inverted_index']
collection_pr = db['page_rank']

def get_docs_by_word(word):
    document = collection_ii.find_one({"word": word})
    if document:
        return document['postings']
    else:
        return None

def get_rank_by_doc(filename):
    document = collection_pr.find_one({"filename": filename})
    if document:
        return document['rank']
    else:
        return None

# word_to_search = 'example'  
# postings_list = get_docs_by_word(word_to_search)
# if postings_list is not None:
#     print(f'Postings for the word "{word_to_search}": {postings_list}')
# else:
#     print(f'No postings found for the word "{word_to_search}".')

# document_to_search = 'file_1.txt'  
# page_rank = get_rank_by_doc(document_to_search)
# if page_rank is not None:
#     print(f'PageRank for "{document_to_search}": {page_rank}')
# else:
#     print(f'No PageRank found for the document "{document_to_search}".')