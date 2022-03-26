from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from profiles.models import FavoriteMovie
from .models import Movie


# Create your views here.
class MovieListView(ListView):
    model = Movie
    template_name = "movies/movies_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        favorite_movies = FavoriteMovie.objects.filter(user=self.request.user)
        favorite_movies = [movie.movie for movie in favorite_movies]
        # top_movies est renvoyé en tant que Queryset pour pouvoir utiliser
        # l'annotation
        top_movies = Movie.objects.annotate(num_favorites=Count("favorite_movie")).order_by("-num_favorites")[:5]
        print(top_movies)
        for movie in top_movies:
            print(movie.title_vf, movie.num_favorites)
        context.update({"favorite_movies": favorite_movies,
                        "top_movies": top_movies})
        return context
