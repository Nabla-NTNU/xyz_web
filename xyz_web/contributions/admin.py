from django.contrib import admin
from .models import Contribution, Vote

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
