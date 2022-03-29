from django.urls import path

from .views import (
    MovieRequestCreateView,
    BluRayRequestCreateView,
    PeopleRequestCreateView,
    MovieRequestView,
    BluRayRequestView,
    PeopleRequestView
)

# Création d'un espace de noms
app_name = 'user_requests'

urlpatterns = [path('add-a-bluray/',
                    BluRayRequestCreateView.as_view(),
                    name="bluray_request_create"),
               path('bluray/<int:pk>/', BluRayRequestView.as_view(),
                    name="bluray_request_detail"),
               path('add-a-movie/',
                    MovieRequestCreateView.as_view(),
                    name="movie_request_create"),
               path('add-a-people/',
                    PeopleRequestCreateView.as_view(),
                    name="people_request_create"),
]
