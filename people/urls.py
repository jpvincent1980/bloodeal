from django.urls import path

from .views import PeopleListView, PeopleDetailView


# Création d'un espace de noms
app_name = 'people'

urlpatterns = [path('list/', PeopleListView.as_view(), name='people_list'),
               path('<str:slug>/<int:pk>/', PeopleDetailView.as_view(), name='people_detail'),
]
