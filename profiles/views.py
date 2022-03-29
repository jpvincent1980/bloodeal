import datetime

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from django.template.response import TemplateResponse

from accounts.forms import CustomUserChangeForm, CustomUserChangePasswordForm
from accounts.models import CustomUser
from blurays.models import BluRay
from movies.models import Movie
from user_requests.forms import BluRayCreationForm, MovieCreationForm, \
    PeopleCreationForm
from .models import FavoriteMovie, FavoritePeople, FavoriteBluRay, FavoriteUser


# Create your views here.
class FavoriteView(ListView):
    queryset = FavoriteMovie.objects.none()
    template_name = "profiles/favorites_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteView, self).get_context_data(**kwargs)
        favorite_movies = FavoriteMovie.objects.filter(user=self.request.user)
        favorite_movies = [movie.movie for movie in favorite_movies]
        favorite_people = FavoritePeople.objects.filter(user=self.request.user)
        favorite_people = [people.people for people in favorite_people]
        favorite_blurays = FavoriteBluRay.objects.filter(user=self.request.user)
        favorite_blurays = [blu_ray.blu_ray for blu_ray in favorite_blurays]
        favorite_users = FavoriteUser.objects.filter(user=self.request.user)
        favorite_users = [user.followed_user for user in favorite_users]
        latest_movies = Movie.objects.all().order_by("-date_created")
        all_blurays = BluRay.objects.all()
        latest_blurays = all_blurays.filter(
            release_date__lte=datetime.date.today()).order_by("-release_date")
        next_blurays = all_blurays.filter(
            release_date__gte=datetime.date.today()).order_by("release_date")
        context.update({"favorite_movies": favorite_movies,
                        "favorite_people": favorite_people,
                        "favorite_blurays": favorite_blurays,
                        "favorite_users": favorite_users,
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


class ProfileList(ListView):
    model = CustomUser
    template_name = "profiles/users_list.html"
    fields = ["email", "pseudo", "first_name", "last_name"]


class ProfileUpdate(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    second_form_class = CustomUserChangePasswordForm
    template_name = "profiles/user_update.html"
    success_url = reverse_lazy("accounts:dashboard")
    message = None

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        elif isinstance(form_class, PasswordChangeForm):
            return CustomUserChangePasswordForm(user=self.request.user,
                                                data=self.request.POST)
        return form_class(**self.get_form_kwargs())

    def get_second_form_class(self):
        return self.second_form_class

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.form_class
        if "form2" not in context:
            context["form2"] = CustomUserChangePasswordForm(user=self.request.user)
        latest_movies = Movie.objects.all().order_by("-date_created")
        all_blurays = BluRay.objects.all()
        latest_blurays = all_blurays.filter(
            release_date__lte=datetime.date.today()).order_by(
            "-release_date")
        next_blurays = all_blurays.filter(
            release_date__gte=datetime.date.today()).order_by(
            "release_date")
        context.update({"latest_movie": latest_movies[0],
                        "latest_bluray": latest_blurays[0],
                        "next_bluray": next_blurays[0],
                        })
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

    def form_valid(self, form):
        """
        If the form is valid, redirect to the dashboard with context message
        """
        form.save()
        print(form)
        if "form2" in self.request.POST:
            update_session_auth_hash(self.request, form.user)
        return HttpResponseRedirect(reverse_lazy("accounts:dashboard"))

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        # Get the user instance
        self.object = self.get_object()

        # Determine which form is submitted by user by using name of
        # the submit button
        if "form" in request.POST:
            # Get the first form
            form_class = self.get_form_class()
            form_name = "form"
            form = self.get_form(form_class)
            # Validate the form
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(**{form_name: form})
        else:
            # Get the second form
            form_name = "form2"
            form = CustomUserChangePasswordForm(user=self.request.user,
                                                data=self.request.POST)
            # Validate the form
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(**{form_name: form})
