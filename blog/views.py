from django.views import generic, View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from blog.lib.session_checks import post_liked, get_ip
from blog.lib.validate_recaptcha import validate_recaptcha
from blog.lib import github_getter

from .models import Post, Comment, InfoPage, PostLike
from .forms import PostForm, CommentForm


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            obj = get_object_or_404(self.model, slug=self.kwargs['slug'])
            context['obj'] = obj
            context['type'] = self.kwargs['type']
        return context

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            query = get_object_or_404(self.model, slug=slug).get_related_posts().filter(is_published=True)
        else:
            query = Post.objects.published()
        return query


class DetailView(View):
    disqus_enabled = settings.ENABLE_DISQUS

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        liked = post_liked(request, slug)
        absolute_url = request.build_absolute_uri()
        context = {'post': post, 'liked': liked, 'absolute_url': absolute_url}
        if self.disqus_enabled:
            form = CommentForm()
            context['form'] = form
        if not post.is_published and not request.user.is_authenticated:
            raise Http404
        return render(request, 'blog/single.html', context)

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if self.disqus_enabled:
            form = CommentForm(request.POST)
            if form.is_valid() and validate_recaptcha(request):
                comment = form.save(commit=False)
                messages.success(request, 'New comment added with success!')
                comment.post = post
                comment.save()
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return redirect(post.get_absolute_url())


@method_decorator(login_required, name='dispatch')
class PostDraftList(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    queryset = Post.objects.drafted()


def new_commits(request):
    commits = github_getter.get_commits()
    return render(request, 'blog/news.html', {'commits': commits})


def info_page(request, slug):
    page = get_object_or_404(InfoPage, slug=slug)
    return render(request, 'blog/info-page.html', {'page': page})


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


def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    response = redirect(post.get_absolute_url())
    if 'liked_posts' in request.session:
        if slug in request.session['liked_posts']:
            return response
        request.session['liked_posts'].append(slug)
        request.session.save()
    else:
        request.session['liked_posts'] = [slug, ]
        request.session.save()
    like = PostLike()
    like.post = post
    like.liked_date = timezone.now()
    like.user_ip = get_ip(request)
    like.save()
    return response


class PostLikeToggle(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        if 'liked_posts' in self.request.session:
            if slug in self.request.session['liked_posts']:
                return url_
            self.request.session['liked_posts'].append(slug)
            self.request.session.save()
        else:
            self.request.session['liked_posts'] = [slug, ]
            self.request.session.save()
        like = PostLike()
        like.post = obj
        like.liked_date = timezone.now()
        like.user_ip = get_ip(self.request)
        like.save()
        return url_


class PostLikeAPIToggle(APIView):
    """
    Adds like to post with given slug.

    * Can't like more than once in one session.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, slug=None):
        obj = get_object_or_404(Post, slug=slug)
        s = request.session.get('liked_posts', '')
        if s:
            if slug in s:
                updated = True
                liked = False
                return Response({'updated': updated, 'liked': liked, })
            self.request.session['liked_posts'].append(slug)
            self.request.session.save()
        else:
            self.request.session['liked_posts'] = [slug, ]
            self.request.session.save()
        like = PostLike()
        like.post = obj
        like.liked_date = timezone.now()
        like.user_ip = get_ip(self.request)
        like.save()
        liked = True
        updated = True
        data = {
            'updated': updated,
            'liked': liked,
        }
        return Response(data)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
