from django.contrib import messages
from django.views.generic import ListView, DetailView

from profiles.models import get_user_all_favorites
from deals.models import Deal
from blurays.models import BluRay, get_blurays
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total
from .models import Movie, get_movies


# Create your views here.
class MovieListView(ListView):
    model = Movie
    template_name = "movies/movies_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context.update(get_movies(self.request.user))
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user))
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
        movie_blurays = BluRay.objects.filter(movie=self.object)
        deals = Deal.objects.filter(bluray__in=movie_blurays)
        context.update({"movie_blurays": movie_blurays,
                        "deals": deals})
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        context.update(get_user_requests_total(self.request.user))
        # Récupère un message à afficher dans la fenêtre modale le cas échéant
        storage = messages.get_messages(self.request)
        if storage:
            context.update({"modal": "modal.html",
                            "modal_content": storage})
        return super().get_context_data(**context)
