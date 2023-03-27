from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=120)
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    is_hit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def director_name(self):
        try:
            return self.director.name
        except:
            return ''

    @property
    def genre_list(self):
        return [genre.name for genre in self.genres.all()]

    @property
    def filter_reviews(self):
        return self.reviews.filter(stars__gt=3)


class Review(models.Model):
    CHOICES = ((i, '* ' * i) for i in range(1, 6))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='reviews')
    stars = models.IntegerField(choices=CHOICES)
    text = models.TextField()

    def __str__(self):
        return self.text
