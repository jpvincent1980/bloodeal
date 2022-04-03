from django.urls import path

from deals.views import DealListView, DealCreateView, DealDetailView

# Création d'un espace de noms
app_name = "deals"

urlpatterns = [path("list/", DealListView.as_view(), name="deals_list"),
               path("<int:pk>/", DealDetailView.as_view(), name="deals_detail"),
               path("create/", DealCreateView.as_view(), name="deals_create")]
