from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('article/new/', views.create_post, name='create-post'),
    path('article/<slug:slug>/', views.DetailView.as_view(), name='article-detail'),
    path('article/<slug:slug>/edit/', views.edit_post, name='article-edit'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='by-category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='by-tag'),
    path('author/<slug:slug>/', views.PseudoView.as_view(), name='by-author'),
]
app_name = 'blog'
