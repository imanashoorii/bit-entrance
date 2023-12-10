# myapp/models.py

from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(6)])
