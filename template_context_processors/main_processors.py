from blog.models import Category
from blog.models import Post
from django.contrib import auth
from django.conf import settings


def get_categories(request):
    dic = Category.objects.all()
    return {"category_list": dic}


def get_drafted_posts_count(request):
    return {"drafted_posts_count": Post.objects.drafted().count()}


def get_username(request):
    return {"username": auth.get_user(request).username}


def is_disqus_enabled(request):
    return {'disqus_enabled': settings.ENABLE_DISQUS}
