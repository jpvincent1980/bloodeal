from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import LoginForm, SignupForm


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
            login_message = f"Adresse email et/ou mot de passe non  valide."
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
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        else:
            login_form = LoginForm(auto_id="login_%s")
            print(signup_form.errors)
            print(signup_form.error_messages)
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
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse('accounts:dashboard'))


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
    context = {}
    return render(request, "accounts/dashboard.html", context)
