from django.urls import path
from django.views.generic.edit import CreateView

from .views import MainView, VoteView, confirm
from .models import Contribution, Vote

urlpatterns = [
    path('', MainView.as_view()),
    path('vote/', VoteView.as_view(), name='vote'),
    path('add/', CreateView.as_view(
        model=Contribution,
        fields='__all__',
        success_url='/'
    ), name='add'),
    path('confirm/<token>/', confirm),
]
