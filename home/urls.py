# home/urls.py

from django.urls import path
from . import views



urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/partial/', views.blog_list_partial, name='blog_list_partial'),
    path('blog/<slug:post_slug>/', views.blog_detail, name='blog_detail'),

    # Videos
    path('videos/', views.video_list, name='video_list'),
    path('videos/partial/', views.video_list_partial, name='video_list_partial'),
    path('videos/<slug:video_slug>/', views.video_detail, name='video_detail'),

    # About
    path('about/', views.about_detail, name='about_detail'),

    # Contact & Subscribe (AJAX)
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
]