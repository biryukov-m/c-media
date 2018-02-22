from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('article/<slug:slug>/', views.DetailView.as_view(), name='article-detail'),
]
