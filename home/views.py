# home/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import (
    PostCategory, Post, Subscriber, AboutPage,
    Video, VideoCategory
)
import logging

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
def home(request):
    return render(request, 'index.html')


# ------------------------------------------------------------------
# BLOG LIST – FULL PAGE
# ------------------------------------------------------------------
def blog_list(request):
    post_list = Post.objects.filter(is_published=True)\
                            .select_related('category')\
                            .order_by('-published_date')

    categories = PostCategory.objects.all()

    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        post_list = post_list.filter(category__slug=category_slug)
    if featured:
        post_list = post_list.filter(is_featured=True)
    
    has_featured = Post.objects.filter(is_published=True, is_featured=True).exists()

    paginator = Paginator(post_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'posts': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'has_featured': has_featured,
    }
    return render(request, 'blog_list.html', context)


# ------------------------------------------------------------------
# BLOG LIST – PARTIAL (HTMX only)
# ------------------------------------------------------------------
def blog_list_partial(request):
    if not request.headers.get('HX-Request'):
        return redirect(f"{reverse('blog_list')}?{request.META['QUERY_STRING']}")

    post_list = Post.objects.filter(is_published=True)\
                            .select_related('category')\
                            .order_by('-published_date')

    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        post_list = post_list.filter(category__slug=category_slug)
    if featured:
        post_list = post_list.filter(is_featured=True)

    paginator = Paginator(post_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    # RECALCULATE has_featured EVERY TIME
    has_featured = Post.objects.filter(is_published=True, is_featured=True).exists()

    context = {
        'posts': page_obj,
        'categories': PostCategory.objects.all(),
        'active_category': category_slug,
        'has_featured': has_featured,  # <-- ALWAYS FRESH
    }
    return render(request, 'partials/blog_list_content.html', context)


# ------------------------------------------------------------------
# BLOG DETAIL
# ------------------------------------------------------------------
def blog_detail(request, post_slug):
    post = get_object_or_404(
        Post.objects.prefetch_related('content_blocks'),
        slug=post_slug,
        is_published=True
    )
    context = {'post': post}
    return render(request, 'blog_detail.html', context)


# ------------------------------------------------------------------
# ABOUT PAGE
# ------------------------------------------------------------------
def about_detail(request):
    try:
        about_page = AboutPage.objects.first()
    except Exception as e:
        logger.error(f"Error loading about page: {str(e)}")
        about_page = None

    context = {'about_page': about_page}
    return render(request, 'about_detail.html', context)


# ------------------------------------------------------------------
# VIDEO LIST – FULL PAGE
# ------------------------------------------------------------------
def video_list(request):
    videos_list = Video.objects.select_related('category')\
                               .filter(is_published=True)\
                               .order_by('-published_date')

    categories = VideoCategory.objects.all()

    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        videos_list = videos_list.filter(category__slug=category_slug)
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    has_featured = Post.objects.filter(is_published=True, is_featured=True).exists()

    paginator = Paginator(videos_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'videos': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'has_featured': has_featured,
    }
    return render(request, 'video_list.html', context)


# ------------------------------------------------------------------
# VIDEO LIST – PARTIAL (HTMX only)
# ------------------------------------------------------------------
def video_list_partial(request):
    if not request.headers.get('HX-Request'):
        return redirect(f"{reverse('video_list')}?{request.META['QUERY_STRING']}")

    videos_list = Video.objects.select_related('category')\
                               .filter(is_published=True)\
                               .order_by('-published_date')

    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        videos_list = videos_list.filter(category__slug=category_slug)
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    paginator = Paginator(videos_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    # RECALCULATE has_featured EVERY TIME
    has_featured = Video.objects.filter(is_published=True, is_featured=True).exists()

    context = {
        'videos': page_obj,
        'categories': VideoCategory.objects.all(),
        'active_category': category_slug,
        'has_featured': has_featured,  # <-- ALWAYS FRESH
    }
    return render(request, 'partials/video_list_content.html', context)


# ------------------------------------------------------------------
# VIDEO DETAIL
# ------------------------------------------------------------------
def video_detail(request, video_slug):
    video = get_object_or_404(Video, slug=video_slug, is_published=True)
    related_videos = Video.objects.filter(
        category=video.category, is_published=True
    ).exclude(id=video.id)[:3]

    context = {
        'video': video,
        'related_videos': related_videos,
    }
    return render(request, 'video_detail.html', context)


# ------------------------------------------------------------------
# CONTACT FORM (AJAX)
# ------------------------------------------------------------------
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)

        try:
            send_mail(
                subject=f'New Contact Form Submission from {name}',
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({
                'success': True,
                'message': 'Your message has been sent successfully.'
            })
        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Error sending message. Try again later.'
            }, status=500)

    return render(request, 'index.html')


# ------------------------------------------------------------------
# SUBSCRIBE (AJAX)
# ------------------------------------------------------------------
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'message': 'Valid email required.'}, status=400)

        try:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                send_mail(
                    subject='Subscription Successful!',
                    message='Thank you for subscribing. You will receive updates on new posts.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                return JsonResponse({'success': True, 'message': 'Subscription successful!'})
            else:
                return JsonResponse({'success': True, 'message': 'You are already subscribed!'})
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            return JsonResponse({'success': False, 'message': 'Error. Try again.'}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=405)