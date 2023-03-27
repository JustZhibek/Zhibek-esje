from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie.models import Movie
from movie.serializers import MovieSerializer, MovieValidateSerializer


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'text': "Hello World",
        'int': 23412,
        'float': 5.55,
        'bool': True,
        'list': [1, 2, 3],
        'dict': {'key': 'value'}
    }
    return Response(data=dict_)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)  # {"name":"asdfasd", "director_id":100}
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        pprint(serializer.validated_data)
        name = serializer.validated_data.get('name')
        duration = serializer.validated_data.get('duration')
        description = serializer.validated_data.get('description') # None
        is_hit = serializer.validated_data.get('is_hit')  # None
        rating = serializer.validated_data.get('rating')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        movie = Movie.objects.create(name=name, duration=duration, description=description,
                                     is_hit=is_hit, rating=rating, director_id=director_id)
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieSerializer(movie).data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.name = serializer.validated_data.get('name')
        movie.duration = serializer.validated_data.get('duration')
        movie.description = serializer.validated_data.get('description')
        movie.is_hit = serializer.validated_data.get('is_hit')
        movie.rating = serializer.validated_data.get('rating')
        movie.director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieSerializer(movie).data)
