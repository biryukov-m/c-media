from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField


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
    def is_published(self):
        return self.filter(published=True).order_by('-pub_date')

    def is_drafted(self):
        return self.filter(published=False).order_by('-pub_date')


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=130, unique=True, default='', verbose_name='URL')
    text = RichTextUploadingField(blank=True, default='', max_length=60000, verbose_name='Статья')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    pub_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    pseudo = models.ForeignKey(Pseudo, on_delete=models.PROTECT, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, verbose_name='Ключевые слова')
    objects = PostManager()
    published = models.BooleanField(default=False)

    def publish(self):
        self.published = True
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

    def get_preview(self):
        return self.text.split('</p>')[0][3:]

    def get_likes(self):
        return self.postlike_set.all().order_by('-liked_date')

    def __str__(self):
        return self.title


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


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(verbose_name='Дата и время', default=timezone.now)
    user_ip = models.GenericIPAddressField(verbose_name='IP посетителя')


class InfoPage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = RichTextUploadingField(verbose_name="Содержимое")
    slug = models.CharField(max_length=50, verbose_name="URL")

    def __str__(self):
        return self.title
