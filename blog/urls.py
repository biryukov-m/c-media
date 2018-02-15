from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test),
    path('question/<int:question_id>/', views.test),
    path('login/', views.test),
    path('signup/', views.test),
    path('ask/', views.test),
    path('popular/', views.test),
    path('new/', views.test),
]
