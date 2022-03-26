from django.views.generic import ListView

from .models import BluRay


# Create your views here.
class BluRayListView(ListView):
    model = BluRay
    template_name = "blurays/blurays_list.html"
