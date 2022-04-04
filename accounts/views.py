from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView

from accounts.forms import LoginForm, SignupForm
from deals.models import get_deals, get_user_favorites_deals
from movies.models import get_movies, get_movies_results
from blurays.models import get_blurays, BluRay, get_blurays_results
from people.models import get_people_results
from profiles.models import get_user_all_favorites, get_user_suggested_blurays
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total, get_user_requests


# Create your views here.
def index_view(request):
    """
    A function-based view that redirects to two different views:
    -> login_view if user is not authenticated
    -> dashboard_view if user is authenticated

    Template:
        None
    """
    next_url = request.GET.get("next", "accounts:dashboard")
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    elif request.method == "POST" and request.POST["button"] == "Je me connecte":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            login_form = LoginForm(auto_id="login_%s")
            signup_form = SignupForm(auto_id="signup_%s")
            login_message = "Adresse email et/ou mot de passe non  valide."
            context = {"login_form": login_form,
                       "signup_form": signup_form,
                       "login_message": login_message,
                       "next": next_url}
            return render(request, "accounts/index.html", context)
    elif request.method == "POST" and request.POST["button"] == "Je m'inscris":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = request.POST["email"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            message = "Merci de votre inscription !"
            storage = [message]
            context = {"modal": "modal.html",
                       "modal_content": storage}
            # Récupère les données pour le bloc de droite
            context.update(get_movies(request.user))
            context.update(get_blurays(request.user))
            # Récupère les données pour le bloc de gauche
            requests_forms = generate_initialized_request_forms(request.user)
            context.update(requests_forms)
            # Récupère les données pour le bloc central
            context.update(get_user_all_favorites(request.user))
            # Récupère le nombre de demandes de l'utilisateur
            context.update(get_user_requests_total(request.user,
                                                   only_open=True))
            return render(request, "accounts/dashboard.html", context)
        else:
            login_form = LoginForm(auto_id="login_%s")
            context = {"login_form": login_form,
                       "signup_form": signup_form}
            return render(request, "accounts/index.html", context)
    else:
        login_form = LoginForm(auto_id="login_%s")
        signup_form = SignupForm(auto_id="signup_%s")
        context = {"login_form": login_form,
                   "signup_form": signup_form}
        return render(request, "accounts/index.html", context)


def login_view(request):
    """
    A function-based view for user to login.

    Context:
        next: next url to redirect user once logged in
        form:  :form:"accounts.LoginForm"
        message: A string displayed to ask user to login

    Template:
        :template:"accounts/login.html"
    """
    next_url = request.GET.get("next", "accounts:dashboard")
    context = {"next": next_url}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            form = LoginForm
            context["form"] = form
            context["message"] = "Adresse email ou mot de passe non valide."
            return render(request, "accounts/login.html", context)
    else:
        form = LoginForm()
        context["form"] = form
        return render(request, "accounts/login.html", context)


class SignupView(CreateView):
    """
    A class-based view for a visitor to signup.

    Context:
        form:  :form:"accounts.SignupForm"

    Template:
        :template:"accounts/signup.html"
    """
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = "../account-created/"

    def form_valid(self, form):
        # Override form_valid function from parent class to add automatic login
        # after signup
        form.save()
        username = self.request.POST["email"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        message = "Merci de votre inscription !"
        storage = [message]
        context = {"modal": "modal.html",
                   "modal_content": storage}
        # Récupère le nombre de demandes de l'utilisateur
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        return render(self.request, "accounts/dashboard.html", context)


@login_required
def account_created_view(request):
    """
    A function-based view to display a confirmation message once user account
    has been created.

    Context:
        None

    Template:
        :template:"accounts/account-created.html"
    """
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
    return render(request, "accounts/account-created.html", context)


def logout_view(request):
    """
    A function-based view to logout user.

    Context:
        None

    Template:
        None
    """
    logout(request)
    return redirect("accounts:index")


def dashboard_view(request):
    # Récupère les données pour le bloc de droite
    context = get_deals()
    context.update(get_movies(request.user))
    context.update(get_blurays(request.user))
    # Récupère les données pour le bloc de gauche
    requests_forms = generate_initialized_request_forms(request.user)
    context.update(requests_forms)
    # Récupère les blu-rays recommandés selon les favoris de l'utilisateur
    context.update(get_user_all_favorites(request.user))
    # Récupère les bons plans recommandés selon les favoris de l'utilisateur
    context.update(get_user_favorites_deals(request.user))
    # # Récupère les suggestions de blurays pour l'utilisateur
    context.update(get_user_suggested_blurays(request.user))
    # Récupère les messages le cas échéant et les envoie à la fenêtre modale
    storage = messages.get_messages(request)
    if storage:
        context.update({"modal": "modal.html",
                        "modal_content": storage})
    # Récupère le nombre de demandes de l'utilisateur
    context.update(get_user_requests(request.user, only_open=True))
    # Récupère le nombre de demandes de l'utilisateur pour la navbar
    context.update(get_user_requests_total(request.user, only_open=True))
    return render(request, "accounts/dashboard.html", context)


class SearchResultsView(ListView):
    template_name = "accounts/search_results.html"
    queryset = BluRay.objects.filter(movie__title_vf="Dune")

    def get_keyword(self):
        return self.request.GET.get("Q", "")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        # Récupère le mot clé du champ de recherche
        keyword = self.get_keyword()
        context.update({"keyword": keyword})
        # Récupère les données pour le bloc de gauche
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        # Récupère les données pour le bloc de droite
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        # Récupère les données pour le bloc central
        context.update(get_user_all_favorites(self.request.user))
        # Récupère les données de recherche pour les blu-rays
        context.update(get_blurays_results(keyword))
        # Récupère les données de recherche pour les films
        context.update(get_movies_results(keyword))
        # Récupère les données de recherche pour les personnalités
        context.update(get_people_results(keyword))
        return context


def sentry_error(request):
    return 1/0
