import sys

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import (CheckboxSelectMultiple, Form, ModelChoiceField,
                          ModelForm, ModelMultipleChoiceField, RadioSelect)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import mark_safe, format_html
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Contribution, Vote

from datetime import datetime


class ConfirmView(TemplateView):
    template_name = "contributions/confirm_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        the_class = getattr(sys.modules[__name__], kwargs["class_name"])
        the_object = the_class.objects.get(confirmation_token=kwargs["token"])
        if not the_object.confirmed:
            the_object.confirm()
            context["action"] = "bekreftet."
        else:
            context["action"] = "allerede bekreftet fra før."

        context["object_name"] = the_class._meta.verbose_name
        return context


class ContributionPlayerLabelMixin:
    def label_from_instance(self, obj):
        return format_html("<span class='contribution--name'>{}</span>{}",
                           obj.name,
                           mark_safe(obj.video_player())
                           )  # TODO: Think really hard about this mark_safe


class RadioSelectCustomOption(RadioSelect):
    """RadioSelect widget where order of label and input in template is reversed."""

    option_template_name = "contributions/input_option_reversed.html"


class VoteChoiceField(ContributionPlayerLabelMixin, ModelChoiceField):
    widget = RadioSelectCustomOption

    def __init__(self, *args, **kwargs):
        # TODO: There has to be a more elegant way to to this.
        # This is a hack.
        kwargs["queryset"] = kwargs["queryset"].filter(approved=True)
        return super().__init__(*args, **kwargs)


class ContributionApproveField(ContributionPlayerLabelMixin, ModelMultipleChoiceField):
    widget = CheckboxSelectMultiple


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ["username", "contribution"]
        field_classes = {"contribution": VoteChoiceField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shuffle order of contributions
        self.fields["contribution"].queryset = self.fields[
            "contribution"
        ].queryset.order_by("?")


class VoteView(CreateView):
    form_class = VoteForm
    success_url = reverse_lazy("vote")
    model = Vote

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        deadline_contribution = datetime(2020, 10, 31, hour=23, minute=59, second=59)
        deadline_vote = datetime(2020, 11, 9, hour=23, minute=59, second=59)
        context["voting_active"] = datetime.now() < deadline_vote
        context["contributing_active"] = datetime.now() < deadline_contribution
        return context


class ContributionApproveForm(Form):
    contributions = ContributionApproveField(
        queryset=Contribution.objects.filter(approved=False, confirmed=True)
    )


class ApproveContributionView(LoginRequiredMixin, FormView):
    form_class = ContributionApproveForm
    success_url = "/approve/"
    template_name = "contributions/contribution_approve.html"

    def form_valid(self, form):
        approved_contributions = form.cleaned_data["contributions"]
        for contribution in approved_contributions:
            contribution.approved = True
            contribution.save()
        # Log out user
        logout(self.request)
        return super().form_valid(form)


class VoteCountView(UserPassesTestMixin, ListView):
    model = Contribution
    template_name="contributions/vote_count.html"

    def test_func(self):
        return self.request.user.is_staff
