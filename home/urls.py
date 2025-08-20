# myapp/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.home, name='home'),
    
    # About URL
    path('about/', views.about_detail, name='about_detail'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('blog/<slug:post_slug>/', views.blog_detail, name='blog_detail'),

    # Video URLs
    path('videos/', views.video_list, name='video_list'),
    path('videos/<slug:video_slug>/', views.video_detail, name='video_detail'),
    
    # Contact URL
    path('contact/', views.contact, name='contact'),

    path('subscribe/', views.subscribe, name='subscribe'),
]