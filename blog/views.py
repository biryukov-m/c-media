from .models import Post, Category, Tag, Pseudo
from django.utils import timezone
from django.views import generic
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "автор"
        return context


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def publish_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect(post.get_absolute_url())


class PostDraftList(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.exclude(pub_date__lt=timezone.now()).order_by('-pub_date')[:10]
