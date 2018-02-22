from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/single.html'

#
# def single(request, article_pk):
#     post = get_object_or_404(Post, pk=article_pk)
#     return render(request, 'blog/single.html', {'post': post})
