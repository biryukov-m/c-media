from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag, Pseudo
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


class CategoryView(generic.DetailView):
    model = Category
    template_name = 'blog/by_attribute.html'
    # context_object_name = object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "категория"
        return context


class TagView(generic.DetailView):
    model = Tag
    template_name = 'blog/by_attribute.html'
    # context_object_name = object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "#тэг"
        context['style'] = True
        return context


class PseudoView(generic.DetailView):
    model = Pseudo
    template_name = 'blog/by_attribute.html'
    # context_object_name = object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "автор"
        return context


#
# def single(request, article_pk):
#     post = get_object_or_404(Post, pk=article_pk)
#     return render(request, 'blog/single.html', {'post': post})
