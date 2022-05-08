from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.test import APITestCase
from moviesApi.constant import API_KEY
from moviesApi.models import Movies, MovieSerializer
from moviesApi.query_data import search_movie_api


class GetAllMoviesPagination(APITestCase):
    """ Test module for GET all movies API """

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.DEFAULT_URL = 'http://127.0.0.1:8000/api/'
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

    def test_get_all_movies(self):
        # get API response
        response = self.client.get(f'{self.DEFAULT_URL}2')
        # get data from db
        movies = Movies.objects.all().order_by('title')
        paginator = Paginator(movies, per_page=10)
        target_page = paginator.get_page(2)
        serialized_page = MovieSerializer(target_page, many=True)
        serialized_page_list = [dict(x) for x in serialized_page.data]
        self.assertEqual(response.data, serialized_page_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_movie(self):
        title = 'becoming bond'
        # get API response
        response = self.client.get(f"{self.DEFAULT_URL}{title.replace(' ', '%20')}")
        # get data from db
        movie = Movies.objects.get(titleSearch=title.replace(' ', ''))
        self.assertEqual(response.data, MovieSerializer(movie).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_movie(self):
        title = 'harry potter'
        # get API response
        response = self.client.post(f"{self.DEFAULT_URL}{title}")
        # get data from db
        name_format = title.lower().capitalize().replace(' ', '%20')
        search_url = f'https://omdbapi.com/?s=%22{name_format}%22&apikey={API_KEY}'
        search_result = search_movie_api(search_url)
        response_list = list(response.data.values())
        all_titles = [item for sublist in response_list for item in sublist]
        self.assertEqual(all_titles, search_result)

    def test_delete_movie_unauthorized(self):
        movie = Movies.objects.order_by('title').first()
        # get API response
        response = self.client.delete(f"{self.DEFAULT_URL}{movie.id}")
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_movie_authorized(self):
        self.user.is_superuser = True
        self.user.save()
        movie = Movies.objects.order_by('title').first()
        # get API response
        response = self.client.delete(f"{self.DEFAULT_URL}{movie.id}")
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
