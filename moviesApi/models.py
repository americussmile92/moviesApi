import uuid
from django.db import models
from rest_framework import serializers


class Movies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    poster = models.CharField(max_length=255)
    titleSearch = models.CharField(max_length=255)

    class Meta:
        unique_together = ('title', 'year',)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('id', 'title', 'year', 'type', 'poster')
