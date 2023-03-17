from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=120)
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    is_hit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
