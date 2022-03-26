from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash, login
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView

from accounts.forms import CustomUserChangeForm, CustomUserChangePasswordForm
from accounts.models import CustomUser
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
        favorite_blu_rays = FavoriteBluRay.objects.filter(user=self.request.user)
        favorite_blu_rays = [blu_ray.blu_ray for blu_ray in favorite_blu_rays]
        favorite_users = FavoriteUser.objects.filter(user=self.request.user)
        favorite_users = [user.followed_user for user in favorite_users]
        context.update({"favorite_movies": favorite_movies,
                        "favorite_people": favorite_people,
                        "favorite_blu_rays": favorite_blu_rays,
                        "favorite_users": favorite_users})
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
    success_url = reverse_lazy("accounts:index")

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
        return context

    # def form_valid(self, form):
    #     form.save()
    #     # Updating the password logs out all other sessions for the user
    #     # except the current one.
    #     update_session_auth_hash(self.request, form.user)
    #     return super(ProfileUpdate, self).form_valid(form)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        print(request.POST)
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
                form.save()
                print(hasattr(form.user, "get_session_auth_hash"))
                print(self.request.user == form.user)
                print(form.user)
                update_session_auth_hash(self.request, form.user)
                return self.form_valid(form)
            else:
                return self.form_invalid(**{form_name: form})
