from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie.models import Movie
from movie.serializers import MovieSerializer


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
        name = request.data.get('name')
        duration = request.data.get('duration')
        description = request.data.get('description')
        is_hit = request.data.get('is_hit')
        rating = request.data.get('rating')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')
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
        movie.name = request.data.get('name')
        movie.duration = request.data.get('duration')
        movie.description = request.data.get('description')
        movie.is_hit = request.data.get('is_hit')
        movie.rating = request.data.get('rating')
        movie.director_id = request.data.get('director_id')
        genres = request.data.get('genres')
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieSerializer(movie).data)