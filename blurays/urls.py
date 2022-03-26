from django.urls import path

from blurays.views import BluRayListView


# Création d'un espace de noms
app_name = 'blurays'

urlpatterns = [path('list/', BluRayListView.as_view(), name="blurays_list"),
]
