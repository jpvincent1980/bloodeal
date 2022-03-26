from django.shortcuts import render
from django.views.generic import ListView

from .models import Deal


# Create your views here.
class DealListView(ListView):
    model = Deal
    template_name = "deals/deals_list.html"
