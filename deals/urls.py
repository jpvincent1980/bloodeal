from django.urls import path

from deals.views import DealListView


# Création d'un espace de noms
app_name = 'deals'

urlpatterns = [path('list/', DealListView.as_view(), name="deals_list"),
]
