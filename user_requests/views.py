from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import MovieRequest, BluRayRequest, PeopleRequest
from .forms import BluRayCreationForm


# Create your views here.
class MovieRequestCreateView(CreateView):
    model = MovieRequest
    fields = ["imdb_link", "status", "user"]
    template_name = "user_requests/movie_request_create.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["created_by"] = self.request.user.pk
        initial["status"] = "1"
        return initial

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie_request_form"] = context["form"]
        return context


class MovieRequestView(DetailView):
    model = MovieRequest


class BluRayRequestCreateView(CreateView):
    model = BluRayRequest
    form_class = BluRayCreationForm
    template_name = "user_requests/bluray_request_create.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["user"] = self.request.user.pk
        initial["status"] = "1"
        return initial

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bluray_request_form"] = context["form"]
        return context


class BluRayRequestView(DetailView):
    model = BluRayRequest


class PeopleRequestCreateView(CreateView):
    model = PeopleRequest
    fields = ["imdb_link", "status", "user"]
    template_name = "user_requests/people_request_create.html"
    success_url = reverse_lazy("accounts:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["user"] = self.request.user.pk
        initial["status"] = "1"
        return initial

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_request_form"] = context["form"]
        return context


class PeopleRequestView(DetailView):
    model = PeopleRequest

