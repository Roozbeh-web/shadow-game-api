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
    baseline_vector = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - profile"

class Scenario(models.Model):
    PRESENCE_CHOICES = [
        ('latent', "Latent"),
        ('stirring', "Stirring"),
        ('born', "Born"),
    ]
    slug = models.SlugField(unique=True)
    chapter = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    shadow_presence = models.CharField(max_length=10, choices=PRESENCE_CHOICES, default="latent")
    is_ending = models.BooleanField(default=False)
    dimension = models.CharField(max_length=20)
    text = models.TextField()
    shadow_text = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.slug} (order {self.order})"

class ChoiceOption(models.Model):
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name="options"
    )
    text = models.CharField(max_length=255)
    delta = models.IntegerField()
    next_scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="incoming",
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.scenario.slug} - option {self.order}"

class Ending(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    shadow_dominant_dimension = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PlayThrough(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playthroughs",
    )
    current_scenario = models.ForeignKey(
        Scenario,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+"
    )
    user_vector = models.JSONField(default=dict)
    shadow_vector = models.JSONField(default=dict)
    distance = models.FloatField(default=0.0)
    user_path = models.JSONField(default=list)
    shadow_path = models.JSONField(default=list)
    ending = models.ForeignKey(
        Ending,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "finished" if self.finished_at else "in progress"
        return f"{self.user.username} - {status}"

class ShadowDecision(models.Model):
    playthrough = models.ForeignKey(
        PlayThrough,
        on_delete=models.CASCADE,
        related_name="shadow_decisions"
    )
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
    )
    option_index = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.playthrough.user.username} - {self.scenario.slug}"
