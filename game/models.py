from django.conf import settings
from django.db import models

class Assessment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assessments',
    )
    raw_answers = models.JSONField()
    scores = models.JSONField()
    version = models.IntegerField(default=1)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - assessment v(self.version)"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    user_vector = models.JSONField(default=dict)
    shadow_vector = models.JSONField(default=dict)
    distance = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - profile"

class Scenario(models.Model):
    slug = models.SlugField(unique=True)
    chapter = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    text = models.TextField()
    shadow_text = models.TextField()
    dimension = models.CharField(max_length=20)
    option = models.JSONField()

    class Meta:
        ordering = ['chapter', 'order']

    def __str__(self):
        return f"{self.slug} (ch{self.chapter}.{self.order})"

class Choice(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    option_index = models.IntegerField()
    reaction_time_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} - {self.scenario.slug} - option {self.option_index}"

    