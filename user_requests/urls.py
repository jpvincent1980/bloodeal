from django.urls import path

from .views import (
    MovieRequestCreateView,
    BluRayRequestCreateView,
    PeopleRequestCreateView,
    UserRequestListView,
    DealRequestCreateView)

# Création d'un espace de noms
app_name = 'user_requests'

urlpatterns = [path('<int:pk>/',
                    UserRequestListView.as_view(),
                    name="user_requests"),
               path('add-a-bluray/',
                    BluRayRequestCreateView.as_view(),
                    name="bluray_request_create"),
               path('add-a-movie/',
                    MovieRequestCreateView.as_view(),
                    name="movie_request_create"),
               path('add-a-people/',
                    PeopleRequestCreateView.as_view(),
                    name="people_request_create"),
               path('add-a-deal/',
                    DealRequestCreateView.as_view(),
                    name="deal_request_create"),
]
