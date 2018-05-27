from django.urls import path, include
from .views import (
    IndexView,
    PostDraftList,
    create_post,
    detail_view,
    publish_post,
    edit_post,
    remove_post,
    like_post,
    CategoryView,
    TagView,
    PseudoView,
    comment_approve,
    comment_remove,
    new_commits,
    info_page,
    PostLikeToggle,
    PostLikeAPIToggle
)


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('draft/', PostDraftList.as_view(), name='post-draft-list'),
    path('article/new/', create_post, name='create-post'),
    path('article/<slug:slug>/', detail_view, name='article-detail'),
    path('article/<slug:slug>/publish/', publish_post, name='publish-post'),
    path('article/<slug:slug>/edit/', edit_post, name='article-edit'),
    path('article/<slug:slug>/remove/', remove_post, name='article-remove'),
    # path('article/<slug:slug>/like/', like_post, name='article-like'),
    path('article/<slug:slug>/like/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/article/<slug:slug>/like/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='by-category'),
    path('tag/<slug:slug>/', TagView.as_view(), name='by-tag'),
    path('author/<slug:slug>/', PseudoView.as_view(), name='by-author'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('news/', new_commits, name='news'),
    path('about/', info_page, {'slug': 'about'}, name='about'),
]
app_name = 'blog'
