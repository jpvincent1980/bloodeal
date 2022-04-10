from django.urls import path

from deals.views import DealListView
from .views import (
    index_view,
    SignupView,
    account_created_view,
    login_view,
    logout_view,
    dashboard_view,
    SearchResultsView,
    help_view,
    contact_view, send_message_view, DeleteAccountView)

# Création d'un espace de noms
app_name = 'accounts'

urlpatterns = [
    path('', DealListView.as_view(), name="index"),
    path('authenticate', index_view, name="authenticate"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account-created/', account_created_view, name="account_created"),
    path('delete-account/<int:pk>/', DeleteAccountView.as_view(), name="delete_account"),
    path('login/', login_view, name="login"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('logout/', logout_view, name="logout"),
    path('search/', SearchResultsView.as_view(), name="search_results"),
    path('help/', help_view, name="help"),
    path('contact/', contact_view, name="contact"),
    path('send-message/', send_message_view, name="send_message")]
