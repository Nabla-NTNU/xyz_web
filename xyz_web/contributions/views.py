from django.forms import ModelForm, ModelChoiceField, RadioSelect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Contribution, Vote
from django.utils.html import mark_safe
from django.urls import reverse_lazy
from django.shortcuts import redirect


def confirm(request, token):
    # TODO: handle object not found
    Vote.objects.get(confirmation_token=token).confirm()
    return redirect('vote')


class MainView(ListView):
    model = Contribution

class VoteChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return mark_safe(obj.video_player() + str(obj.number_of_votes()))

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['username', 'contribution']
        widgets = {'contribution': RadioSelect}
        field_classes = {'contribution': VoteChoiceField}

class VoteView(CreateView):
    form_class = VoteForm
    success_url = reverse_lazy('vote')
    model = Vote
