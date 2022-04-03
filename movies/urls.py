from django.urls import path

from movies.views import MovieListView, MovieDetailView


# Création d'un espace de noms
app_name = 'movies'

urlpatterns = [path("list/", MovieListView.as_view(), name="movies_list"),
               path("<str:slug>/<int:pk>/", MovieDetailView.as_view(), name="movies_detail")]
