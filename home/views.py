from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Category, Post, Tag, Subscriber, AboutPage, Video, VideoCategory
import logging
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

# Render static pages
def home(request):
    return render(request, 'index.html')


# Blog list with categories and recent posts
def blog_list(request):
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True)[:6]

    context = {
        'categories': categories,
        'recent_posts': recent_posts,
    }

    return render(request, 'blog_list.html', context)


def blog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    post_list = Post.objects.filter(
        category=category, 
        is_published=True
    ).order_by('-created_at')

    paginator = Paginator(post_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': page_obj, 
    }

    return render(request, 'blog_category.html', context)

# Blog detail with next/previous and related posts
def blog_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, is_published=True)

    context = {
        'post': post,
    }

    return render(request, 'blog_detail.html', context)

# About page detail view
def about_detail(request):
    # Get the about page content or create a default one if it doesn't exist
    try:
        about_page = AboutPage.objects.first()
    except Exception as e:
        logger.error(f"Error loading about page: {str(e)}")
        about_page = None

    context = {
        'about_page': about_page
    }

    return render(request, 'about_detail.html', context)

# Video list with categories
def video_list(request):
    """
    Display a list of videos, with optional filtering by category or featured status.
    """
    # ADDED: .select_related('category') for performance
    videos_list = Video.objects.select_related('category').all().order_by('-published_date')
    categories = VideoCategory.objects.all()

    # Filtering logic (this part is good)
    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        # No need for a separate get_object_or_404 query here
        # The filter will handle it. If you need the category object, you can get it.
        videos_list = videos_list.filter(category__slug=category_slug)
    
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    # Pagination setup (this part is good)
    paginator = Paginator(videos_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'videos': page_obj,
        'categories': categories,
        'active_category': category_slug,
    }
    return render(request, 'video_list.html', context)


def video_detail(request, video_slug):
    """
    Display a single video in detail.
    """
    video = get_object_or_404(Video, slug=video_slug)
    
    # Optional: Get related videos from the same category
    related_videos = Video.objects.filter(category=video.category).exclude(id=video.id)[:3]

    context = {
        'video': video,
        'related_videos': related_videos,
    }
    return render(request, 'video_detail.html', context)

# Contact form handling via AJAX
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
            logger.error(f"Error sending contact form email: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'There was an error sending your message. Please try again later.'
            }, status=500)

    return render(request, 'index.html')

# REMOVED: @csrf_exempt decorator. Frontend JavaScript must now send the CSRF token.
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email.'}, status=400)

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
                return JsonResponse({'success': True, 'message': 'Subscription successful! Check your inbox.'})
            else:
                return JsonResponse({'success': True, 'message': 'You are already subscribed!'})
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            return JsonResponse({'success': False, 'message': 'Error occurred. Try again later.'}, status=500)
    return JsonResponse({'message': 'Invalid request'}, status=405)