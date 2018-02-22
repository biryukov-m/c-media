from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('article/<slug:slug>/', views.DetailView.as_view(), name='article-detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='by-category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='by-tag'),
    path('author/<slug:slug>/', views.PseudoView.as_view(), name='by-author'),
]
