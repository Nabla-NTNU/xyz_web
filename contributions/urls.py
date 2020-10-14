from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .models import Contribution, Vote
from .views import ApproveContributionView, ConfirmView, VoteView

urlpatterns = [
    path("", VoteView.as_view(), name="vote"),
    path(
        "add/",
        CreateView.as_view(
            model=Contribution,
            fields=["name", "username", "video_link"],
            success_url=reverse_lazy("thanks"),
        ),
        name="add",
    ),
    path(
        "thanks-for-contributing/",
        TemplateView.as_view(
            template_name="contributions/thanks.html",
        ),
        name="thanks",
    ),
    path("approve/", ApproveContributionView.as_view(), name='approve'),
    path("confirm/<class_name>/<token>/", ConfirmView.as_view()),
]
