from .models import Post, Category, Tag, Pseudo
from django.utils import timezone
from django.views import generic
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.published()

# На всякий случай
class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/single.html'


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/single.html', {'post': post, 'form': form})


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
        return context


class PseudoView(generic.DetailView):
    model = Pseudo
    template_name = 'blog/by_attribute.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "автор"
        return context


@login_required
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


@login_required
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


@login_required
def publish_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect(post.get_absolute_url())


@login_required
def remove_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('blog:home')


@method_decorator(login_required, name='dispatch')
class PostDraftList(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.drafted()
