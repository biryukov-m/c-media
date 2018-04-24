from .models import Post, Category, Tag, Pseudo, Comment
from django.utils import timezone
from django.views import generic
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.objects.is_published()


class CategoryView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_attribute = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['model_attribute'] = model_attribute
        context['type'] = "категория"
        return context

    def get_queryset(self):
        query = get_object_or_404(Category, slug=self.kwargs['slug'])
        return query.get_related_posts()


class TagView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_attribute = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['model_attribute'] = model_attribute
        context['type'] = "#тэг"
        return context

    def get_queryset(self):
        query = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return query.get_related_posts()


class PseudoView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_attribute = get_object_or_404(Pseudo, slug=self.kwargs['slug'])
        context['model_attribute'] = model_attribute
        context['type'] = "автор"
        return context

    def get_queryset(self):
        query = get_object_or_404(Pseudo, slug=self.kwargs['slug'])
        return query.get_related_posts()


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            req = requests.post(url, data=values)
            res = req.json()
            print(type(res))
            print(res)
            print(res['success'])
            ''' End reCAPTCHA validation '''
            if res['success']:
                comment = form.save(commit=False)
                messages.success(request, 'New comment added with success!')
                comment.post = post
                comment.save()
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/single.html', {'post': post, 'form': form})


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
    queryset = Post.objects.is_drafted()


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
