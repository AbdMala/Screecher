from django.contrib.auth.models import User
from django.db import models


class Screech(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    private = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
