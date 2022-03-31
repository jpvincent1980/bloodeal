from django.db.models import Count
from django.views.generic import ListView, DetailView

from deals.models import get_deals
from movies.models import get_movies
from user_requests.forms import generate_initialized_request_forms
from user_requests.models import get_user_requests_total
from .models import BluRay, get_blurays


# Create your views here.
class BluRayListView(ListView):
    model = BluRay
    template_name = "blurays/blurays_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BluRayListView, self).get_context_data(**kwargs)
        context.update(get_blurays(self.request.user))
        requests_forms = generate_initialized_request_forms(self.request.user)
        context.update(requests_forms)
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        return context


class BluRayDetailView(DetailView):
    model = BluRay
    template_name = "blurays/blurays_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BluRayDetailView, self).get_context_data(**kwargs)
        context.update(get_movies(self.request.user))
        context.update(get_blurays(self.request.user))
        context.update(get_user_requests_total(self.request.user,
                                               only_open=True))
        context.update(get_deals(self.object))
        print(context)
        return context
