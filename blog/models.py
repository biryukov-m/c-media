from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=60, unique=True, default='')

    def get_related_posts(self):
        query = self.post_set.all().order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class Pseudo(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=60, unique=True, default='')
    create_date = models.DateField(auto_created=True)

    def get_related_posts(self):
        query = self.post_set.all().order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=60, unique=True, default='')

    def get_related_posts(self):
        query = self.post_set.all().order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=130, unique=True, default='')
    text = models.TextField(max_length=60000)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    pseudo = models.ForeignKey(Pseudo, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)

    def ispublished(self):
        try:
            return self.pub_date < timezone.now()
        except TypeError:
            return False

    def publish(self):
        self.pub_date = timezone.now()
        self.save()


    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[str(self.slug)])

    def __str__(self):
        return self.title


class Menu(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=130, unique=True, default='')
    submenu = models.ManyToManyField(Category, default='', blank=True, null=True)

    def __str__(self):
        return self.name
