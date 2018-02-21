from django.urls import path, include
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
]
