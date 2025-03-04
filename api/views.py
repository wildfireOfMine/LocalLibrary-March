from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import AuthorSerializer
from catalog.models import Author

# Create your views here.

@api_view(['GET', 'POST'])
def autor_api_view(request):
    if request.method == "GET":
        autores = Author.objects.all()
        autores_serializer = AuthorSerializer(autores, many=True)
        return Response(autores_serializer.data)
    elif request.method == "POST":
        autores_serializer = AuthorSerializer(data = request.data)
        if autores_serializer.is_valid():
            autores_serializer.save()
            return Response(autores_serializer.data)
        return Response(autores_serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def autor_detail_view(request, pk=None):
    if request.method == "GET":
        autor = Author.objects.filter(id=pk)
        autor_serializer = AuthorSerializer(autor, many=True)
        return Response(autor_serializer.data)
    elif request.method == "PUT":
        autor = Author.objects.filter(id=pk).first()
        autor_serializer = AuthorSerializer(autor, data = request.data)
        if autor_serializer.is_valid():
            autor_serializer.save()
            return Response(autor_serializer.data)
        return Response(autor_serializer.errors)
    elif request.method == "DELETE":
        autor = Author.objects.filter(id=pk)
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)