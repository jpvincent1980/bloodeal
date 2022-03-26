from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView)

from .views import ProfileList, ProfileUpdate, FavoriteView

# Création d'un espace de noms
app_name = 'profiles'

urlpatterns = [path('list/', ProfileList.as_view(), name="profiles_list"),
               path('update/', ProfileUpdate.as_view(), name="profile_update"),
               # If urls are in a urls config with an app_name, success_url
               # must be given as an argument in the as_view function.
               # Otherwise, no argument has to be given if password_change_done
               # is in the same urls.py file without app_name.
               path('change-password/<int:toto>/', PasswordChangeView.as_view(success_url=reverse_lazy('profiles:password_change_done')), name="change-password"),
               path('change-password-done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
               path('reset-password/', PasswordResetView.as_view(success_url=reverse_lazy('profiles:password_reset_done')), name="password_reset"),
               path('reset-password-done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
               path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('profiles:password_reset_complete')), name="password_reset_confirm"),
               path('reset-password-complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
               path('favorites/', FavoriteView.as_view(), name="favorites_list"),
]
