from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from blurays.models import get_blurays, BluRay
from movies.models import get_movies, Movie
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total
from .models import Deal


# Create your views here.
class DealListView(ListView):
    model = Deal
    template_name = "deals/deals_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealListView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        context.update({"user_deals": user_deals})
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        return context


class DealDetailView(DetailView):
    model = Deal
    template_name = "deals/deals_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealDetailView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        bluray = BluRay.objects.filter(deal_blu_ray=self.object)
        movie = Movie.objects.filter(bluray_movie__in=bluray)
        movie = movie[0] if movie else movie
        context.update({"user_deals": user_deals,
                        "movie": movie})
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
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
        message = "Merci pour ce bon plan ! Nous allons procéder à sa vérification."
        messages.add_message(self.request,
                             level=messages.INFO,
                             message=message)
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealCreateView, self).get_context_data(**kwargs)
        user_deals = Deal.objects.filter(created_by=self.request.user).order_by("-date_created")
        context.update({"user_deals": user_deals})
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        return context
