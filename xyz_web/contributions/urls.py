from django.urls import path
from django.views.generic.edit import CreateView

from . import views
from .models import Contribution

urlpatterns = [
    path('', views.MainView.as_view()),
    path('add/', CreateView.as_view(
        model=Contribution,
        fields='__all__',
        success_url='/'
    )),
    path('confirm/<token>/', views.confirm),
]
