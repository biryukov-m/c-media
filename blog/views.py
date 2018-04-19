from .models import Post, Category, Tag, Pseudo, Comment
from django.utils import timezone
from django.views import generic
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1
    queryset = Post.objects.published()



# def index_view(request):
#     queryset = Post.objects.published()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 10)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)
#     return render(request, 'blog/index.html', {'posts': posts})



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
            post = form.save()
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


def vote_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.likes += 1
    post.save()
    return redirect(post.get_absolute_url())


@method_decorator(login_required, name='dispatch')
class PostDraftList(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.drafted()


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('blog:article-detail', slug=comment.post.slug)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    slug = comment.post.slug
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('blog:article-detail', slug=slug)
