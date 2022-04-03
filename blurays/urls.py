from django.urls import path

from blurays.views import BluRayListView, BluRayDetailView

# Création d'un espace de noms
app_name = 'blurays'

urlpatterns = [path('list/', BluRayListView.as_view(), name="blurays_list"),
               path('<str:slug>/<int:pk>/', BluRayDetailView.as_view(), name="blurays_detail")]
