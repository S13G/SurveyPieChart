from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
