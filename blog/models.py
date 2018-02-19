from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Pseudo(models.Model):
    name = models.CharField(max_length=20)
    create_date = models.DateField(auto_created=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=30000)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    pub_date = models.DateTimeField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    pseudo = models.ForeignKey(Pseudo, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
