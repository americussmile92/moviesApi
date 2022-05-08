import uuid

from django.db import transaction, migrations

from moviesApi.constant import API_KEY
from moviesApi.models import Movies
from moviesApi.query_data import search_movie_api


def get_one_hundred_movies(apps, schema_editor):
    movies = {}
    page_count = 1
    while len(list(movies.keys())) < 100:
        url = f'http://www.omdbapi.com/?apikey={API_KEY}&s=*bond*&page={page_count}'
        json_response = search_movie_api(url, [])
        for e in json_response:
            movies[e['Title']] = e
        page_count += 1
    movies_list = list(movies.values())
    if len(movies_list) > 100:
        movies_list = movies_list[:100]
    movies_data = [Movies(
        uuid.uuid4(),
        e['Title'],
        e['Year'],
        e['Type'],
        e['Poster'],
        e['Title'].lower().replace(" ", "")) for e in movies_list]
    with transaction.atomic():
        Movies.objects.bulk_create(movies_data)


class Migration(migrations.Migration):
    dependencies = [('moviesApi', '0001_initial')]

    operations = [
        migrations.RunPython(get_one_hundred_movies)
    ]
