from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Contribution


def confirm(request, token):
    return "ff"


class MainView(ListView):
    model = Contribution

class AddContributionView(CreateView):
    model = Contribution
