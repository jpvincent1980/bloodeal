from django.urls import path

from .views import (
    index_view,
    SignupView,
    account_created_view,
    login_view,
    logout_view,
    dashboard_view,
    SearchResultsView)

# Création d'un espace de noms
app_name = 'accounts'

urlpatterns = [
    path('', index_view, name="index"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account-created/', account_created_view, name="account-created"),
    path('login/', login_view, name="login"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('logout/', logout_view, name="logout"),
    path('search/', SearchResultsView.as_view(), name="search_results")]
