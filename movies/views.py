import datetime

from django.db.models import Count
from django.views.generic import ListView, DetailView

from profiles.models import FavoriteMovie
from deals.models import Deal
from blurays.models import BluRay
from user_requests.forms import BluRayCreationForm, MovieCreationForm, \
    PeopleCreationForm
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
        context.update({"favorite_movies": favorite_movies,
                        "top_movies": top_movies})
        bluray_request_form = BluRayCreationForm(initial={"user": self.request.user,
                                                          "status": "1"})
        movie_request_form = MovieCreationForm(initial={"user": self.request.user,
                                                        "status": "1"})
        people_creation_form = PeopleCreationForm(
            initial={"user": self.request.user,
                     "status": "1"})
        requests_forms = {"bluray_request_form": bluray_request_form,
                          "movie_request_form": movie_request_form,
                          "people_request_form": people_creation_form}
        context.update(requests_forms)
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movies_detail.html"

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        blurays = BluRay.objects.filter(movie=self.object)
        deals = Deal.objects.filter(blu_ray__in=blurays)
        favorite_movies = FavoriteMovie.objects.filter(user=self.request.user)
        favorite_movies = [movie.movie for movie in favorite_movies]
        latest_movies = Movie.objects.all().order_by("-date_created")
        all_blurays = BluRay.objects.all()
        latest_blurays = all_blurays.filter(
            release_date__lte=datetime.date.today()).order_by("-release_date")
        next_blurays = all_blurays.filter(
            release_date__gte=datetime.date.today()).order_by("release_date")
        context.update({"blurays": blurays,
                        "deals": deals,
                        "favorite_movies": favorite_movies,
                        "latest_movie": latest_movies[0],
                        "latest_bluray": latest_blurays[0],
                        "next_bluray": next_blurays[0],
                        })
        return super().get_context_data(**context)

