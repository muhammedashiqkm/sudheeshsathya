from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
# REMOVED: from django.views.decorators.csrf import csrf_exempt (No longer needed)
from .models import Category, Post, Tag, Subscriber, AboutPage, Video, VideoCategory
import logging
# ADDED: Paginator for improved page loading
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

# Render static pages
def home(request):
    return render(request, 'index.html')

def blog(request):
    return render(request, 'blog.html')

# Blog list with categories and recent posts
def blog_list(request):
    # ADDED: Pagination logic
    post_list = Post.objects.filter(is_published=True)
    paginator = Paginator(post_list, 9) # Show 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True)[:6]

    context = {
        'categories': categories,
        'recent_posts': recent_posts,
        'posts': page_obj,  # Use the paginated object
    }

    return render(request, 'blog_list.html', context)

# Blog posts by category
def blog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    # ADDED: Pagination for category pages
    post_list = Post.objects.filter(category=category, is_published=True)
    paginator = Paginator(post_list, 9) # Show 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': page_obj, # Use the paginated object
    }

    return render(request, 'blog_category.html', context)

# Blog detail with next/previous and related posts
def blog_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, is_published=True)

    previous_post = Post.objects.filter(
        created_at__lt=post.created_at,
        is_published=True
    ).order_by('-created_at').first()

    next_post = Post.objects.filter(
        created_at__gt=post.created_at,
        is_published=True
    ).order_by('created_at').first()

    related_posts = post.get_related_posts()

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'related_posts': related_posts,
    }

    return render(request, 'blog_detail.html', context)

# About page detail view
def about_detail(request):
    # Get the about page content or create a default one if it doesn't exist
    try:
        about_page = AboutPage.objects.first()
        if not about_page:
            about_page = AboutPage.objects.create(
                title="Who Is Dan Koe?",
                subtitle="Just a human obsessed with humans.",
                content="I'm the author of The Art of Focus, co-founder of Kortex, and writer obsessed with the mind, the internet, and the future.\n\nPreviously, I was a brand advisor for creators and influencers. Now I teach writing as a way to discover your life's work, secure your future, and enjoy a creative lifestyle.\n\nAs a brand advisor, I would help influencers systemize their workflow. They often were overworked, underrested, and needed a drastic change in how they view creativity. It's difficult to get people to see that they don't need to work more than ~4 hours a day to get the results they want, but once they understand it, they can't remember why they ever worked longer than that."
            )
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
    videos_list = Video.objects.all().order_by('-published_date')
    categories = VideoCategory.objects.all()

    # Filtering logic
    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        category = get_object_or_404(VideoCategory, slug=category_slug)
        videos_list = videos_list.filter(category=category)
    
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    # IMPROVEMENT: Pagination is now active
    paginator = Paginator(videos_list, 9) # Show 9 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'videos': page_obj, # Use the paginated object
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
# REMOVED: @csrf_exempt decorator. Frontend JavaScript must now send the CSRF token.
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