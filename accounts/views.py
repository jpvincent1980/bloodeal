import smtplib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from accounts.models import CustomUser
from bloodeal.settings import EMAIL_HOST_USER
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
            context.update(get_user_requests_total(request.user))

            return render(request, "accounts/dashboard.html", context)

        else:
            login_form = LoginForm(auto_id="login_%s")
            context = {"login_form": login_form,
                       "signup_form": signup_form}
            storage = messages.get_messages(request)
            if storage:
                context.update({"modal": "modal.html",
                                "modal_content": storage})

            return render(request, "accounts/index.html", context)

    else:
        login_form = LoginForm(auto_id="login_%s")
        signup_form = SignupForm(auto_id="signup_%s")
        context = {"login_form": login_form,
                   "signup_form": signup_form}
        # Récupère les messages le cas échéant et les envoie à la
        # fenêtre modale
        storage = messages.get_messages(request)

        if storage:
            context.update({"modal": "modal.html",
                            "modal_content": storage})

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
        context.update(get_user_requests_total(self.request.user))

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


class DeleteAccountView(DeleteView):
    """
    A class-based view for a user to delete his/her account.

    Context:
        form:  :form:"accounts.SignupForm"

    Template:
        :template:"accounts/delete-account.html"
    """
    model = CustomUser
    # form_class = DeleteAccountForm
    template_name = "accounts/delete-account.html"
    success_url = reverse_lazy("accounts:index")

    def post(self, request, *args, **kwargs):
        # Override form_valid function from parent class to add automatic login
        # after signup
        if self.kwargs.get("pk") == self.request.user.pk:
            message = "Votre compte a bien été supprimé ! A bientôt !"
            messages.add_message(self.request,
                                 level=messages.INFO,
                                 message=message)
            user = CustomUser.objects.filter(pk=self.request.user.pk)
            user.delete()

            return HttpResponseRedirect(reverse_lazy("accounts:index"))

        else:
            message = "Vous ne pouvez pas supprimé le compte d'un autre."
            messages.add_message(self.request,
                                 level=messages.INFO,
                                 message=message)

            return HttpResponseRedirect(reverse_lazy("accounts:index"))


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


@login_required
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
    context.update(get_user_requests(request.user))
    # Récupère le nombre de demandes de l'utilisateur pour la navbar
    context.update(get_user_requests_total(request.user))

    return render(request, "accounts/dashboard.html", context)


class SearchResultsView(ListView):
    template_name = "accounts/search_results.html"
    queryset = BluRay.objects.none()

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
        # print(context)

        return context


def help_view(request):
    """
    A function-based view to display help message.

    Context:
        None

    Template:
        :template:"accounts/help.html"
    """
    # Récupère les données pour le bloc de droite
    context = get_movies(request.user)
    context.update(get_blurays(request.user))
    # Récupère les données pour le bloc de gauche
    requests_forms = generate_initialized_request_forms(request.user)
    context.update(requests_forms)
    # Récupère le nombre de demandes de l'utilisateur
    context.update(get_user_requests_total(request.user))

    return render(request, "accounts/help.html", context)


def contact_view(request):
    """
    A function-based view to display a contact form.

    Context:
        None

    Template:
        :template:"accounts/help.html"
    """
    # Récupère les données pour le bloc de droite
    context = get_movies(request.user)
    context.update(get_blurays(request.user))
    # Récupère les données pour le bloc de gauche
    requests_forms = generate_initialized_request_forms(request.user)
    context.update(requests_forms)
    # Récupère le nombre de demandes de l'utilisateur
    context.update(get_user_requests_total(request.user))

    return render(request, "accounts/contact.html", context)


@login_required
def send_message_view(request):
    if request.method == "POST":
        # Récupère les données pour le bloc de droite
        context = get_movies(request.user)
        context.update(get_blurays(request.user))
        # Récupère les données pour le bloc de gauche
        requests_forms = generate_initialized_request_forms(request.user)
        context.update(requests_forms)
        # Récupère le nombre de demandes de l'utilisateur
        context.update(get_user_requests_total(request.user))

        if not request.POST.get("formulaire_bloodeal") == "BLOODEAL":
            message = "Seriez-vous un robot ? ... "
            storage = [message]
            context.update({"modal": "modal.html", "modal_content": storage})

            return render(request, "accounts/contact.html", context)

        else:
            formulaire_nom = request.POST.get("formulaire_nom")
            formulaire_email = request.POST.get("formulaire_email")
            formulaire_message = request.POST.get("formulaire_message")

            try:
                message = EmailMultiAlternatives(f"[BLOODEAL] Message de {formulaire_nom}",
                                                 formulaire_message,
                                                 to=["bloodeal@hotmail.com"],
                                                 from_email=EMAIL_HOST_USER,
                                                 reply_to=[formulaire_email])
                message.send()
                message = "Merci de votre message."

            except (smtplib.SMTPServerDisconnected,
                    smtplib.SMTPDataError,
                    ConnectionRefusedError) as error:
                print("L'email n'a pas pu être envoyé.\n", error)
                message = "Désolé, votre message n'a pas pu être envoyé ..."
            storage = [message]
            context.update({"modal": "modal.html", "modal_content": storage})

            return render(request, "accounts/dashboard.html", context)

    else:

        return redirect("accounts:index")


def sentry_error(request):

    return 1 / 0
