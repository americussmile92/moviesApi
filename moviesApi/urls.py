"""movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from moviesApi.views import GetMovies

schema_view = get_schema_view(
   openapi.Info(
      title="Movies API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

movies_page = GetMovies.as_view({'get': 'movies'})
movie_page = GetMovies.as_view({'get': 'movie', 'post': 'movie', 'delete': 'movie'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<int:page_index>/<int:pagesize>/', movies_page),
    path('api/<int:page_index>/<int:pagesize>', movies_page),
    path('api/<int:page_index>/', movies_page),
    path('api/<int:page_index>', movies_page),
    path('api/<int:page_index>', movies_page),
    path('api/<str:movie_name>/', movie_page),
    path('api/<str:movie_name>', movie_page),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
