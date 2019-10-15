from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, choices=[("first", "first_choice")])
