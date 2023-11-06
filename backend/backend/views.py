from django.http import JsonResponse
from rest_framework.decorators import api_view
from backend.models import InvertedIndex
from pymongo import MongoClient

@api_view(['GET'])
def hello(request):
    return JsonResponse({'message': 'Hola'})

@api_view(["POST"])
def search(request):
    # Conectar con la instancia de MongoDB directamente
    client = MongoClient('localhost', 27017)
    db = client['search_engine_db']
    
    # Obtener palabras de la solicitud
    words = request.data.get('words', [])
    
    # Buscar documentos para cada palabra
    documents = {}
    for word in words:
        cursor = db.inverted_index.find({"word": word}, {"_id": 0, "postings": 1})
        documents[word] = list(cursor)

    return JsonResponse(documents)