import uuid

from django.core.paginator import Paginator
from django.db import IntegrityError
from requests import Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from moviesApi.constant import API_KEY
from moviesApi.models import Movies, MovieSerializer
from moviesApi.query_data import search_movie_api


def _get_movie(movie_name: str):
    try:
        format_search_string = movie_name.lower().replace(' ', '')
        movie = Movies.objects.get(titleSearch=format_search_string)
        serialized_movie = MovieSerializer(movie)
        return Response(serialized_movie.data, status=status.HTTP_200_OK)
    except Movies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def _update_movie(movie_name: str):
    name_format = movie_name.lower().capitalize().replace(' ', '%20')
    search_url = f'https://omdbapi.com/?s=%22{name_format}%22&apikey={API_KEY}'
    response = search_movie_api(search_url)
    response_message = {'INSERTED': [], 'DUPLICATION ERROR': [], 'OTHER ERROR': []}
    if response is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # one movie title can have multiple year
    for movie in response:
        try:
            movie_obj = Movies.objects.create(id=uuid.uuid4(),
                                              title=movie['Title'],
                                              year=movie['Year'],
                                              type=movie['Type'],
                                              poster=movie['Poster'],
                                              titleSearch=movie['Title'].lower().replace(" ", "")
                                              )
            if movie_obj:
                response_message['INSERTED'].append(movie)
        except IntegrityError:
            response_message['DUPLICATION ERROR'].append(movie)
        except Exception as ex:
            response_message['OTHER ERROR'].append(movie)
    # if one movie is successfully inserted and one not still return successful
    if response_message['INSERTED']:
        return Response(response_message,
                        status=status.HTTP_200_OK)
    if response_message['DUPLICATION ERROR']:
        return Response(response_message,
                        status=status.HTTP_409_CONFLICT)
    if response_message['OTHER ERROR']:
        return Response(response_message,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _delete_movie(request: Request, id: str):
    try:
        uuid.UUID(id).version
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    current_user = request.user
    if current_user.is_superuser is False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    movie = Movies.objects.get(id=id)
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GetMovies(ModelViewSet):

    def get_serializer_class(self):
        return MovieSerializer

    @action(methods=['get'], detail=False)
    def movies(self, request: Request, page_index: int, page_size: int = 10):
        movies = Movies.objects.all().order_by('title')
        paginator = Paginator(movies, per_page=page_size)
        if page_index > paginator.num_pages:
            return Response({'ERROR': 'page index out of range'}, status=status.HTTP_400_BAD_REQUEST)
        target_page = paginator.get_page(page_index)
        serialized_page = MovieSerializer(target_page, many=True)
        serialized_page_list = [dict(x) for x in serialized_page.data]
        return Response(serialized_page_list, status=status.HTTP_200_OK)

    @action(methods=['get', 'post'], detail=False)
    def movie(self, request: Request, movie_name: str):
        if request.method == 'GET':
            return _get_movie(movie_name)
        if request.method == 'POST':
            return _update_movie(movie_name)
        if request.method == 'DELETE':
            return _delete_movie(request, movie_name)
