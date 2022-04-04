import re

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from blurays.models import get_blurays, BluRay, get_user_requested_blurays
from deals.models import get_deals
from movies.models import get_movies, Movie, get_user_requested_movies
from people.models import People, get_user_requested_people
from profiles.models import get_user_all_favorites
from .models import MovieRequest, BluRayRequest, PeopleRequest, \
    get_user_requests_blurays, get_user_requests_movies, \
    get_user_requests_people, get_user_requests_total, \
    DealRequest, get_user_requests_deals
from .forms import BluRayCreationForm, generate_initialized_request_forms


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
        imdb_link = form["imdb_link"]
        imdb_id = re.search(r"tt[0-9].[^(?:/|?)]+", str(imdb_link))
        if imdb_id:
            duplicate = Movie.objects.filter(imdb_id=imdb_id[0])
            if duplicate:
                message = f"{duplicate[0]} est déjà sur Bloodeal."
                messages.add_message(self.request,
                                     level=messages.INFO,
                                     message=message)
                return HttpResponseRedirect(reverse_lazy("movies:movies_detail",
                                                         kwargs={"slug": duplicate[0].slug,
                                                                 "pk": duplicate[0].pk}))
            else:
                form.save()
                generate_confirmation_message(self.request)
                return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie_request_form"] = context["form"]
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        context.update(get_user_requests_total(self.request.user))
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
        amazon_link = form["amazon_link"]
        amazon_asin = re.search(r"B0[.]*[^(?:/|?)]+", str(amazon_link))
        if amazon_asin:
            duplicate = BluRay.objects.filter(amazon_asin=amazon_asin[0])
            if duplicate:
                message = f"{duplicate[0]} est déjà sur Bloodeal."
                messages.add_message(self.request,
                                     level=messages.INFO,
                                     message=message)
                return HttpResponseRedirect(reverse_lazy("blurays:blurays_detail",
                                                         kwargs={"slug": duplicate[0].slug,
                                                                 "pk": duplicate[0].pk}))
            else:
                form.save()
                generate_confirmation_message(self.request)
                return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bluray_request_form"] = context["form"]
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        context.update(get_user_requests_total(self.request.user))
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
        imdb_link = form["imdb_link"]
        imdb_id = re.search(r"nm[0-9].[^(?:/|?)]+", str(imdb_link))
        if imdb_id:
            duplicate = People.objects.filter(imdb_id=imdb_id[0])
            if duplicate:
                message = f"{duplicate[0]} est déjà sur Bloodeal."
                messages.add_message(self.request,
                                     level=messages.INFO,
                                     message=message)
                return HttpResponseRedirect(reverse_lazy("people:people_detail",
                                                         kwargs={"slug": duplicate[0].slug,
                                                                 "pk": duplicate[0].pk}))
            else:
                form.save()
                generate_confirmation_message(self.request)
                return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people_request_form"] = context["form"]
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        context.update(get_user_requests_total(self.request.user))
        return context


class PeopleRequestView(DetailView):
    model = PeopleRequest


class DealRequestCreateView(CreateView):
    model = DealRequest
    fields = ["amazon_link", "price", "user"]
    template_name = "user_requests/deal_request_create.html"
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
        generate_confirmation_message(self.request)
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deal_request_form"] = context["form"]
        # Récupère les données pour le bloc de gauche
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        context.update(get_user_requests_total(self.request.user))
        return context


class UserRequestListView(ListView):
    template_name = "user_requests/user-requests.html"

    def get(self, request, *args, **kwargs):
        filter = request.GET.get("filter")
        if kwargs["pk"] != self.request.user.pk:
            message = "Vous ne pouvez pas avoir accès aux demandes d'un autre utilisateur."
            messages.add_message(self.request,
                                 level=messages.INFO,
                                 message=message)
            return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))
        else:
            # Récupère les données pour le bloc de droite
            context = get_deals()
            context.update(get_movies(self.request.user))
            context.update(get_blurays(self.request.user))
            # Récupère toutes les demandes de l'utilisateurs
            context.update(get_user_requests_blurays(self.request.user,
                                                     filter))
            context.update(get_user_requests_movies(self.request.user,
                                                    filter))
            context.update(get_user_requests_people(self.request.user,
                                                    filter))
            context.update(get_user_requests_deals(self.request.user,
                                                   filter))
            # Récupère toutes les instances créées suite à une demande de
            # l'utilisateur
            context.update(get_user_requested_blurays(self.request.user))
            context.update(get_user_requested_movies(self.request.user))
            context.update(get_user_requested_people(self.request.user))
            # Récupère les données pour le bloc de gauche
            requests_forms = generate_initialized_request_forms(self.request.user)
            context.update(requests_forms)
            # Récupère les données pour le bloc central
            context.update(get_user_all_favorites(self.request.user))
            context.update(get_user_requests_total(self.request.user))
            return render(request, "user_requests/user-requests.html", context)


def generate_confirmation_message(request, level=messages.INFO):
    message = "Merci pour votre demande. Nous allons procéder à son étude."
    messages.add_message(request, level=level, message=message)
    return True
