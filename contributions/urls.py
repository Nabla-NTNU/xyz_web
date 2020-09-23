from django.urls import path
from django.views.generic.edit import CreateView

from .views import VoteView, confirm, ApproveContributionView
from .models import Contribution, Vote

urlpatterns = [
    path('', VoteView.as_view(), name='vote'),
    path('add/', CreateView.as_view(
        model=Contribution,
        fields=['name', 'username', 'video_link', 'description'],
        success_url='/'
    ), name='add'),
    path('approve/', ApproveContributionView.as_view()),
    path('confirm/<token>/', confirm),
]
