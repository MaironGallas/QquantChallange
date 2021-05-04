from copy import deepcopy

import rispy
from django.contrib.admin import views
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ris.base.models import Articles, Article_Complete
from ris.base.parser import PlainTextParser
from ris.base.serializers import ArticlesSerializer, ArticleFieldSerializer

mapping = deepcopy(rispy.TAG_KEY_MAPPING)
mapping["ID"] = "article_id"

@api_view(['GET', 'POST'])
@parser_classes([PlainTextParser])
def articles_list(request):
    """
    A view that can accept GET and POST requests with PlainText content.
    """
    if request.method == 'GET':
        article = Articles.objects.all()
        serializer = ArticlesSerializer(article, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        entries = rispy.loads(str(request.data.decode('utf-8')))
        for entry in entries:
            dados = {'dados': entry}
            serializer = ArticlesSerializer(data=dados)
            if serializer.is_valid():
                serializer.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([PlainTextParser])
def articles_detail(request, pk):
    try:
        article = Articles.objects.get(pk=pk)
    except Articles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticlesSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        dados = {'dados': rispy.loads(str(request.data.decode('utf-8')))}
        serializer = ArticlesSerializer(article, data=dados)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@parser_classes([PlainTextParser])
def articles_fields_list(request):
    if request.method == 'GET':
        article = Article_Complete.objects.all()
        serializer = ArticleFieldSerializer(article, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        entries = rispy.loads(str(request.data.decode('utf-8')), mapping=mapping)
        for entry in entries:
            serializer = ArticleFieldSerializer(data=entry)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
