from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('draft/', views.PostDraftList.as_view(), name='post-draft-list'),
    path('article/new/', views.create_post, name='create-post'),
    path('article/<slug:slug>/', views.detail_view, name='article-detail'),
    path('article/<slug:slug>/publish/', views.publish_post, name='publish-post'),
    path('article/<slug:slug>/edit/', views.edit_post, name='article-edit'),
    path('article/<slug:slug>/remove/', views.remove_post, name='article-remove'),
    path('article/<slug:slug>/like/', views.like_post, name='article-like'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='by-category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='by-tag'),
    path('author/<slug:slug>/', views.PseudoView.as_view(), name='by-author'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('news/', views.new_commits, name='news'),
    path('about/', views.info_page, {'slug': 'about'}, name='about'),
]
app_name = 'blog'
