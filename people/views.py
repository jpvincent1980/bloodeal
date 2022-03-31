from itertools import chain

from django.views.generic import ListView, DetailView

from deals.models import Deal
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total
from .models import People
from movies.models import Movie, MovieDirector, MovieActor, get_movies
from blurays.models import BluRay, get_blurays


# Create your views here.
class PeopleListView(ListView):
    model = People
    template_name = "people/people_list.html"


class PeopleDetailView(DetailView):
    model = People
    template_name = "people/people_detail.html"

    def get_movies_as_director(self):
        director = People.objects.filter(pk=self.object.pk)
        movies = Movie.objects.filter(movie_director__director=director[0])
        return movies

    def get_movies_as_actor(self):
        actor = People.objects.filter(pk=self.object.pk)
        movies = Movie.objects.filter(movie_actor__actor=actor[0])
        return movies

    # TODO Supprimer les doublons si réalisateur et acteur du même film
    def get_movies(self):
        movies = sorted(chain(self.get_movies_as_director(),
                     self.get_movies_as_actor()),
                      key=lambda movie: movie.release_year,
                      reverse=True)
        return movies

    def get_blurays(self):
        blurays = BluRay.objects.filter(movie__in=self.get_movies())
        return blurays

    # TODO Supprimer les doublons si réalisateur et acteur du même film
    def get_deals(self):
        deals = Deal.objects.filter(blu_ray__in=self.get_blurays())
        return deals

    def get_context_data(self, **kwargs):
        context = super(PeopleDetailView, self).get_context_data()
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        # Le queryset 'movies' ci-dessous qui ne comporte que les films de
        # l'instance de personnalité écrasera le queryset également appelé 'movies'
        # importés plus haut qui contient tous les films
        context.update({"people_movies": self.get_movies(),
                        "people_blurays": self.get_blurays(),
                        "people_deals": self.get_deals()})
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        print(context)
        return context
