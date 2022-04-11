from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.views.decorators.csrf import ensure_csrf_cookie

from accounts.forms import CustomUserChangeForm, CustomUserChangePasswordForm
from accounts.models import CustomUser
from blurays.models import get_blurays, BluRay
from movies.models import get_movies, Movie
from people.models import People
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total
from .models import (FavoriteMovie,
                     FavoritePeople,
                     FavoriteBluRay,
                     get_user_all_favorites,
                     get_user_suggested_blurays)


# Create your views here.
@method_decorator(login_required, name='dispatch')
class FavoriteView(ListView):
    queryset = FavoriteMovie.objects.none()
    template_name = "profiles/favorites_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteView, self).get_context_data(**kwargs)
        favorite_users = CustomUser.objects.filter(user_followed__user=self.request.user)
        context.update({"favorite_users": favorite_users})
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user))

        return context


@method_decorator(login_required, name='dispatch')
class ProfileList(ListView):
    model = CustomUser
    template_name = "profiles/users_list.html"
    fields = ["email", "pseudo", "first_name", "last_name"]


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    second_form_class = CustomUserChangePasswordForm
    template_name = "profiles/user_update.html"
    success_url = reverse_lazy("accounts:dashboard")

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

        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user))

        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to the dashboard with context message
        """
        form.save()
        message = "Vos modifications ont bien été enregistrées."

        if "form2" in self.request.POST:
            update_session_auth_hash(self.request, form.user)
            message = "Votre mot de passe a bien été modifié."

        messages.add_message(self.request,
                             level=messages.INFO,
                             message=message)

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


@ensure_csrf_cookie
# @method_decorator(login_required, name='dispatch')
def add_to_favorite_view(request):
    user = request.user
    type = request.POST.get("type")
    pk = request.POST.get("pk")
    context = request.POST.get("context")

    if user and type and pk:

        if type == "bluray":
            bluray = BluRay.objects.filter(pk=pk)

            if bluray:
                duplicate = FavoriteBluRay.objects.filter(user=user, bluray=bluray[0])

                if duplicate:
                    duplicate.delete()

                else:
                    FavoriteBluRay.objects.create(user=user, bluray=bluray[0])

        elif type == "movie":
            movie = Movie.objects.filter(pk=pk)

            if movie:
                duplicate = FavoriteMovie.objects.filter(user=user, movie=movie[0])

                if duplicate:
                    duplicate.delete()

                else:
                    FavoriteMovie.objects.create(user=user, movie=movie[0])

        else:
            people = People.objects.filter(pk=pk)

            if people:
                duplicate = FavoritePeople.objects.filter(user=user,
                                                          people=people[0])

                if duplicate:
                    duplicate.delete()

                else:
                    FavoritePeople.objects.create(user=user, people=people[0])

    user_all_favorites = get_user_all_favorites(request.user)
    user_suggested_blurays = get_user_suggested_blurays(request.user)

    if context:
        context.update(user_all_favorites)
        context.update(user_suggested_blurays)

    else:
        context = user_all_favorites
        context.update(user_suggested_blurays)

    return redirect("/")
