from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=60, unique=True, default='')

    def get_related_posts(self):
        query = self.post_set.all().filter(is_published=True).order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class Pseudo(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=60, unique=True, default='')
    create_date = models.DateField(auto_created=True)

    def get_related_posts(self):
        query = self.post_set.all().filter(is_published=True).order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=60, unique=True, default='')

    def get_related_posts(self):
        query = self.post_set.all().filter(is_published=True).order_by('-pub_date')
        return query

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    def published(self):
        return self.filter(is_published=True).order_by('-pub_date')

    def drafted(self):
        return self.filter(is_published=False).order_by('-pub_date')


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
    is_published = models.BooleanField(default=False)
    read_time = models.CharField(default='', max_length=20, verbose_name='Время на прочтение')

    def save(self, *args, **kwargs):
        self.update_read_time()
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.is_published = True
        self.pub_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:article-detail', kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse('blog:like-toggle', kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse('blog:like-api-toggle', kwargs={"slug": self.slug})

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

    def get_related_posts(self):
        return self.category.get_related_posts().exclude(id=self.id)[:3]

    def get_word_count(self):
        text = strip_tags(self.text)
        words = text.split(' ')
        return len(words)

    def update_read_time(self):
        min_read_speed = 120
        max_read_speed = 180
        word_count = self.get_word_count()
        min_minutes = round(word_count / max_read_speed)
        max_minutes = round(word_count / min_read_speed)
        if 5 <= max_minutes <= 20 or max_minutes % 10 == 0 or 5 <= max_minutes % 10 <= 9:
            word_ending = ''
        elif 2 <= max_minutes % 10 <= 4:
            word_ending = 'ы'
        elif max_minutes % 10 == 1:
            word_ending = 'а'

        out = "{} - {} минут{}".format(min_minutes, max_minutes, word_ending)
        self.read_time = out

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

    def __str__(self):
        output = ','.join(
            [self.post.title,
             self.liked_date.strftime('%H:%m:%S %e.%m.%y'),
             self.user_ip]
        )
        return output


class InfoPage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = RichTextUploadingField(verbose_name="Содержимое")
    slug = models.CharField(max_length=50, verbose_name="URL")

    def __str__(self):
        return self.title
