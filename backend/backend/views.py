from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.models import InvertedIndex
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient
from .utils import search_query, get_rank_by_doc


@api_view(['GET'])
def hello(request):
    return JsonResponse({'message': 'Hola'})


@api_view(["POST"])
def search(request):
    # Conectar con la instancia de MongoDB directamente
    client = MongoClient('localhost', 27017)
    db = client['search_engine_db']

    page_rank = {}

    words = request.data.get("words", "").lower().split()
    response = search_query(words)
    print("query: ", response)
    pagelist = []

    if not len(response):
        return Response([])

    else:
        for lista in response:
            for page in lista[0]:
                print("pagerank: ", page_rank)
                if page in page_rank:
                    page_rank[page][1] += ' '+lista[1]
                else:
                    curr_rank = get_rank_by_doc(page)
                    if(curr_rank != None):
                        page_rank[page] = [get_rank_by_doc(page), lista[1]]
                    else:
                        page_rank[page] = [0, lista[1]]
                        
    page_rank = {k: v for k, v in sorted(
        page_rank.items(), reverse=True, key=lambda item: item[1][0])}

    if len(page_rank) <= 10:
        pagelist = [[key, page_rank[key]] for key in page_rank]
    else:
        temp_dic = dict(list(page_rank.items())[:10])
        pagelist = [[key, temp_dic[key]] for key in temp_dic]

    return Response(pagelist)
