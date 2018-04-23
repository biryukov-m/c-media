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


class PostManager(models.Manager):
    def published(self):
        return self.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    def drafted(self):
        return self.exclude(pub_date__lte=timezone.now()).order_by('-pub_date')


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=130, unique=True, default='')
    text = models.TextField(max_length=60000)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    pseudo = models.ForeignKey(Pseudo, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    objects = PostManager()

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[str(self.slug)])

    def get_comments(self):
        return self.comment_set.all().order_by('-created_date')

    def get_approved_comments(self):
        return self.comment_set.all().filter(approved_comment=True).order_by('-created_date')

    def get_drafted_comments(self):
        return self.comment_set.all().exclude(approved_comment=True).order_by('-created_date')

    def __str__(self):
        return self.title


class Menu(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=130, unique=True, default='')
    submenu = models.ManyToManyField(Category, default='', blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    email = models.EmailField(null='example@mail.com')
    text = models.TextField(max_length=5000)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return ': '.join([self.author, self.text[0:30]])