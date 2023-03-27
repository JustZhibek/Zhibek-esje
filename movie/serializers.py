from rest_framework import serializers
from .models import Movie, Director, Genre, Review
from rest_framework.exceptions import ValidationError


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


class MovieValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)
    duration = serializers.IntegerField()
    description = serializers.CharField(required=False, default='No description')
    is_hit = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField()  # 100
    rating = serializers.FloatField(min_value=1, max_value=10)
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):  # 100
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError(f'Director with id ({director_id}) not found!')
        return director_id

    def validate_genres(self, genres):
        pass
