from rest_framework import serializers
from .models import Movie, Director, Genre, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text'.split()


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name age'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True)
    director_str = serializers.SerializerMethodField()
    filter_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id name genre_list director_name director_str filter_reviews'.split()
        # exclude = 'id'.split()

    def get_director_str(self, movie):
        return movie.director_name
