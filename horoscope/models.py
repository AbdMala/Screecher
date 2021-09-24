from django.db import models


# Create your models here.
class Sign(models.Model):
    data = models.JSONField()
