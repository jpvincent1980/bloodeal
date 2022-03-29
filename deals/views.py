import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from blurays.models import BluRay
from movies.models import Movie
from user_requests.forms import BluRayCreationForm, PeopleCreationForm, \
    MovieCreationForm
from .models import Deal


# Create your views here.
class DealListView(ListView):
    model = Deal
    template_name = "deals/deals_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealListView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        context.update({"user_deals": user_deals})
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


class DealDetailView(DetailView):
    model = Deal
    template_name = "deals/deals_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealDetailView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        context.update({"user_deals": user_deals,
                        })
        return context


class DealCreateView(CreateView):
    model = Deal
    fields = ["amazon_link", "price", "created_by"]
    template_name = "deals/deals_create.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["created_by"] = self.request.user.pk
        return initial

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealCreateView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        latest_movies = Movie.objects.all().order_by("-date_created")
        all_blurays = BluRay.objects.all()
        latest_blurays = all_blurays.filter(
            release_date__lte=datetime.date.today()).order_by("-release_date")
        next_blurays = all_blurays.filter(
            release_date__gte=datetime.date.today()).order_by("release_date")
        context.update({"user_deals": user_deals,
                        "latest_movie": latest_movies[0],
                        "latest_bluray": latest_blurays[0],
                        "next_bluray": next_blurays[0],
                        })
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
