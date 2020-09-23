from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .views import VoteView, ConfirmView, ApproveContributionView
from .models import Contribution, Vote

urlpatterns = [
    path('', VoteView.as_view(), name='vote'),
    path('add/', CreateView.as_view(
        model=Contribution,
        fields=['name', 'username', 'video_link', 'description'],
        success_url=reverse_lazy('thanks')
    ), name='add'),
    path('thanks-for-contributing/', TemplateView.as_view(
        template_name="contributions/thanks.html",
    ), name='thanks'),
    path('approve/', ApproveContributionView.as_view()),
    path('confirm/<class_name>/<token>/', ConfirmView.as_view()),
]
