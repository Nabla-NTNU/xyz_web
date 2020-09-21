from django.forms import ModelForm, ModelChoiceField, RadioSelect, CheckboxSelectMultiple, Form, ModelMultipleChoiceField
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from .models import Contribution, Vote
from django.utils.html import mark_safe
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


def confirm(request, token):
    # TODO: handle object not found
    Vote.objects.get(confirmation_token=token).confirm()
    return redirect('vote')


class MainView(ListView):
    model = Contribution


class ContributionPlayerLabelMixin:
    def label_from_instance(self, obj):
        return mark_safe(obj.video_player() + str(obj.number_of_votes()))

class VoteChoiceField(ContributionPlayerLabelMixin, ModelChoiceField):
    widget = RadioSelect
    def __init__(self, *args, **kwargs):
        # TODO: There has to be a more elegant way to to this.
        # This is a hack.
        kwargs['queryset'] = kwargs['queryset'].filter(approved=True)
        return super().__init__(*args, **kwargs)


class ContributionApproveField(ContributionPlayerLabelMixin, ModelMultipleChoiceField):
    widget = CheckboxSelectMultiple


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['username', 'contribution']
        field_classes = {'contribution': VoteChoiceField}


class VoteView(CreateView):
    form_class = VoteForm
    success_url = reverse_lazy('vote')
    model = Vote


class ContributionApproveForm(Form):
    contributions = ContributionApproveField(
        queryset=Contribution.objects.filter(approved=False))


class ApproveContributionView(LoginRequiredMixin, FormView):
    form_class = ContributionApproveForm
    success_url = "/approve/"
    template_name = "contributions/contribution_approve.html"

    def form_valid(self, form):
        approved_contributions = form.cleaned_data['contributions']
        for contribution in approved_contributions:
            contribution.approved = True
            contribution.save()
        # Log out user
        logout(self.request)
        return super().form_valid(form)
