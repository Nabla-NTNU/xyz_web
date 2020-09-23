from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Contribution, Vote


@admin.register(Contribution)
class ContributionAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(SimpleHistoryAdmin):
    pass
