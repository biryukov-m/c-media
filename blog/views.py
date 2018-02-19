from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.utils import timezone

# def test(request, *args, **kwargs):
#     return HttpResponse('OK')


def test(request):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
    return render(request, 'blog/index.html', {'posts': posts})


def single(request):
    post = Post.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date').first()
    return render(request, 'blog/single.html', {'post': post})