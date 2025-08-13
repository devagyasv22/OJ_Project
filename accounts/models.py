# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codeforces_handle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username
