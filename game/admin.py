from django.contrib import admin
from .models import (Assessment, Profile, Scenario, ChoiceOption,
                      Ending, PlayThrough, ShadowDecision,
)

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('slug', 'chapter', 'order', 'shadow_presence', 'is_ending', 'dimension')
    list_filter = ('shadow_presence', 'is_ending', 'chapter', 'dimension')
    search_fields = ('slug', 'text')

@admin.register(ChoiceOption)
class ChoiceOptionAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'order', 'text', 'delta', 'next_scenario')

@admin.register(PlayThrough)
class PlaythroughAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_scenario', 'distance', 'started_at', 'finished_at')
    list_filter = ('finished_at',)

@admin.register(ShadowDecision)
class ShadowDecisionAdmin(admin.ModelAdmin):
    list_display = ('playthrough', 'scenario', 'option_index', 'created_at')

admin.site.register(Assessment)
admin.site.register(Profile)


