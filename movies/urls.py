from django.urls import path

from movies.views import MovieListView


# Création d'un espace de noms
app_name = 'movies'

urlpatterns = [path("movies", MovieListView.as_view(), name="movies_list"),
]
