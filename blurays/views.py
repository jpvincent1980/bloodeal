from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView

from deals.models import Deal
from profiles.models import FavoriteBluRay
from user_requests.forms import BluRayCreationForm, MovieCreationForm, \
    PeopleCreationForm
from .models import BluRay


# Create your views here.
class BluRayListView(ListView):
    model = BluRay
    template_name = "blurays/blurays_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BluRayListView, self).get_context_data(**kwargs)
        favorite_blurays = FavoriteBluRay.objects.filter(user=self.request.user)
        favorite_blurays = [blu_ray.blu_ray for blu_ray in favorite_blurays]
        # top_blurays est renvoyé en tant que Queryset pour pouvoir utiliser
        # l'annotation
        top_blurays = BluRay.objects.annotate(num_favorites=Count("favorite_blu_ray")).order_by("-num_favorites")[:5]
        context.update({"favorite_blurays": favorite_blurays,
                        "top_blurays": top_blurays})
        bluray_request_form = BluRayCreationForm(initial={"user": self.request.user,
                                                          "status": "1"},
                                                 auto_id="bluray_request_%s")
        movie_request_form = MovieCreationForm(initial={"user": self.request.user,
                                                        "status": "1"},
                                               auto_id="movie_request_%s")
        people_creation_form = PeopleCreationForm(initial={"user": self.request.user,
                                                           "status": "1"},
                                                  auto_id="people_request_%s")
        requests_forms = {"bluray_request_form": bluray_request_form,
                          "movie_request_form": movie_request_form,
                          "people_request_form": people_creation_form}
        context.update(requests_forms)
        return context


class BluRayDetailView(DetailView):
    model = BluRay
    template_name = "blurays/blurays_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BluRayDetailView, self).get_context_data(**kwargs)
        favorite_blurays = FavoriteBluRay.objects.filter(user=self.request.user)
        favorite_blurays = [blu_ray.blu_ray for blu_ray in favorite_blurays]
        deals_blurays = Deal.objects.filter(blu_ray=self.object)
        # top_blurays est renvoyé en tant que Queryset pour pouvoir utiliser
        # l'annotation
        top_blurays = BluRay.objects.annotate(num_favorites=Count("favorite_blu_ray")).order_by("-num_favorites")[:5]
        context.update({"favorite_blurays": favorite_blurays,
                        "deals_blurays": deals_blurays,
                        "top_blurays": top_blurays})
        return context
