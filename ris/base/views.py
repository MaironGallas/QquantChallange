from copy import deepcopy

import rispy
from django.contrib.admin import views
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.response import Response

from ris.base.models import Article_Complete
from ris.base.parser import PlainTextParser
from ris.base.serializers import ArticleFieldSerializer

mapping = deepcopy(rispy.TAG_KEY_MAPPING)
mapping["ID"] = "article_id"


@api_view(['GET', 'POST'])
@parser_classes([PlainTextParser])
def articles_fields_list(request):
    """
    Esta view recebe um request onde no metodo get devolve todos os artigos cadastrados no banco e
    quando recebe um metodo post cadastra um novo artigo, as entradas devem ser em text/plain no formato de um arquivo
    RIS.
        """
    if request.method == 'GET':
        article = Article_Complete.objects.all()
        serializer = ArticleFieldSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        print(request.data)
        entries = rispy.loads(str(request.data.decode('utf-8')), mapping=mapping)
        for entry in entries:
            serializer = ArticleFieldSerializer(data=entry)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([PlainTextParser])
def articles_detail(request, pk):
    """
    Esta view é responsável por realizar o CRUD dos artigos cadastrados em formato RIS.
        """
    try:
        article = Article_Complete.objects.get(pk=pk)
    except Article_Complete.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleFieldSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        entries = rispy.loads(str(request.data.decode('utf-8')), mapping=mapping)
        serializer = ArticleFieldSerializer(article, data=entries[0])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
