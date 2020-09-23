import sys

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import (CheckboxSelectMultiple, Form, ModelChoiceField,
                          ModelForm, ModelMultipleChoiceField, RadioSelect)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import mark_safe
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .models import Contribution, Vote


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
        return mark_safe(obj.video_player())


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
