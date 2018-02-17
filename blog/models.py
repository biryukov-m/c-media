from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40)


class Pseudo(models.Model):
    name = models.CharField(max_length=20)
    create_date = models.DateField(auto_created=True)


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=30000)
    create_date = models.DateField(blank=True, auto_now_add=True)
    pub_date = models.DateField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    pseudo = models.ForeignKey(Pseudo, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
