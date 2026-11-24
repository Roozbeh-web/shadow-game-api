from django.contrib import admin
from .models import Assessment, Profile, Scenario, Choice

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'version', 'conpleted_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'distance', 'updated_at')

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('slug', 'chapter', 'order', 'dimension')
    list_filter = ('chapter', 'dimension')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'scenario', 'option_index', 'created_at')
    list_filter = ('scenario',)

