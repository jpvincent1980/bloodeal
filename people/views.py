from itertools import chain

from django.views.generic import ListView, DetailView

from deals.models import Deal
from .models import People
from movies.models import Movie, MovieDirector, MovieActor
from blurays.models import BluRay


# Create your views here.
class PeopleListView(ListView):
    model = People
    template_name = "people/people_list.html"


class PeopleDetailView(DetailView):
    model = People
    template_name = "people/people_detail.html"

    def get_movies_as_director(self):
        movies = MovieDirector.objects.filter(director=self.object)
        movies = [movie.movie.pk for movie in movies]
        movies = Movie.objects.filter(id__in=movies)
        return movies

    def get_movies_as_actor(self):
        movies = MovieActor.objects.filter(actor=self.object)
        movies = [movie.movie.pk for movie in movies]
        movies = Movie.objects.filter(id__in=movies)
        return movies

    # TODO Supprimer les doublons si réalisateur et acteur du même film
    def get_movies(self):
        return sorted(chain(self.get_movies_as_director(),
                     self.get_movies_as_actor()),
                      key=lambda movie:movie.release_year,
                      reverse=True)

    def get_blurays_as_director(self):
        movies = MovieDirector.objects.filter(director=self.object)
        movies = [movie.movie.pk for movie in movies]
        movies = Movie.objects.filter(id__in=movies)
        movies = [movie.pk for movie in movies]
        blurays = BluRay.objects.filter(movie__in=movies)
        return blurays

    def get_blurays_as_actor(self):
        movies = MovieActor.objects.filter(actor=self.object)
        movies = [movie.movie.pk for movie in movies]
        movies = Movie.objects.filter(id__in=movies)
        movies = [movie.pk for movie in movies]
        blurays = BluRay.objects.filter(movie__in=movies)
        return blurays

    # TODO Supprimer les doublons si réalisateur et acteur du même film
    def get_blurays(self):
        return sorted(chain(self.get_blurays_as_director(),
                     self.get_blurays_as_actor()))

    def get_deals_as_director(self):
        movies = MovieDirector.objects.filter(director=self.object)
        movies = [movie.movie.pk for movie in movies]
        deals = Deal.objects.filter(blu_ray__movie__in=movies)
        return deals

    def get_deals_as_actor(self):
        movies = MovieActor.objects.filter(actor=self.object)
        movies = [movie.movie.pk for movie in movies]
        deals = Deal.objects.filter(blu_ray__movie__in=movies)
        return deals

    # TODO Supprimer les doublons si réalisateur et acteur du même film
    def get_deals(self):
        return sorted(chain(self.get_deals_as_director(),
                     self.get_deals_as_actor()),
                      key=lambda deal:deal.date_created,
                      reverse=True)

    def get_context_data(self, **kwargs):
        context = super(PeopleDetailView, self).get_context_data()
        context.update({"movies": self.get_movies(),
                        "blurays": self.get_blurays(),
                        "deals": self.get_deals()})
        return context
