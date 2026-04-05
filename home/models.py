# home/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import (
    PostCategory, Post, Subscriber, AboutPage,
    Video, VideoCategory
)
import logging
import resend  # Ensure 'resend' is in your requirements.txt
from background_task import background

logger = logging.getLogger(__name__)

# ==================================================================
# BACKGROUND TASKS (Using Resend API directly to bypass SMTP blocks)
# ==================================================================

@background(schedule=1)
def async_send_contact_email(name, email, message, from_email, contact_email):
    """Handles sending the contact form email via Resend API."""
    resend.api_key = settings.RESEND_API_KEY
    try:
        params = {
            "from": from_email,
            "to": [contact_email],
            "subject": f'New Contact Form Submission from {name}',
            "text": f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        }
        resend.Emails.send(params)
        logger.info(f"Background task: Contact email sent successfully for {name}.")
    except Exception as e:
        logger.error(f"Background task error sending contact email: {str(e)}")
        raise e


@background(schedule=1)
def async_send_subscription_email(user_email, from_email):
    """Sends the welcome email to a new subscriber."""
    resend.api_key = settings.RESEND_API_KEY
    subject = 'Welcome to the Newsletter!'
    
    html_content = """
    <div style="font-family: 'Segoe UI', sans-serif; color: #333; line-height: 1.6;">
        <h2>Newsletter Subscription Successful!</h2>
        <p><strong>Welcome aboard, friend</strong></p>
        <p>I’m glad you’re here — let’s learn to live deliberately.</p>
        <p><strong>Every Saturday at 8 PM</strong>, a quiet reflection awaits you in your inbox.</p>
    </div>
    """

    try:
        params = {
            "from": from_email,
            "to": [user_email],
            "subject": subject,
            "html": html_content,
        }
        resend.Emails.send(params)
        logger.info(f"Background task: Subscription email sent to {user_email}.")
    except Exception as e:
        logger.error(f"Background task error sending subscription email: {e}")
        raise e


@background(schedule=1)
def send_post_notification_email_task(post_id):
    """Broadcasts a new post alert to ALL real active subscribers from the database."""
    resend.api_key = settings.RESEND_API_KEY
    try:
        post = Post.objects.get(pk=post_id)
        # Pull only active subscribers
        subscribers = Subscriber.objects.filter(is_active=True)
        recipient_list = [s.email for s in subscribers]

        if not recipient_list:
            logger.info("No active subscribers found. Skipping broadcast.")
            return

        site_url = settings.SITE_DOMAIN
        post_url = f"{site_url}{reverse('blog_detail', args=[post.slug])}"
        
        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": recipient_list,
            "subject": f"New Post: {post.title}",
            "html": f"""
                <div style="font-family: sans-serif; line-height: 1.6;">
                    <h3>New Article Published!</h3>
                    <p>I just posted: <strong>{post.title}</strong></p>
                    <p>{post.excerpt}</p>
                    <a href="{post_url}" style="padding: 10px 20px; background: #000; color: #fff; text-decoration: none; border-radius: 5px;">Read Full Article</a>
                </div>
            """
        }
        resend.Emails.send(params)
        logger.info(f"Successfully broadcasted post {post_id} to {len(recipient_list)} users.")
    except Exception as e:
        logger.error(f"Broadcast error for post {post_id}: {e}")
        raise e


# ==================================================================
# VIEWS
# ==================================================================

def home(request):
    return render(request, 'index.html')

def blog_list(request):
    post_list = Post.objects.filter(is_published=True).select_related('category').order_by('-published_date')
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

def blog_list_partial(request):
    if not request.headers.get('HX-Request'):
        return redirect(f"{reverse('blog_list')}?{request.META['QUERY_STRING']}")

    post_list = Post.objects.filter(is_published=True).select_related('category').order_by('-published_date')
    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        post_list = post_list.filter(category__slug=category_slug)
    if featured:
        post_list = post_list.filter(is_featured=True)

    paginator = Paginator(post_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    has_featured = Post.objects.filter(is_published=True, is_featured=True).exists()

    context = {
        'posts': page_obj,
        'categories': PostCategory.objects.all(),
        'active_category': category_slug,
        'has_featured': has_featured,
    }
    return render(request, 'partials/blog_list_content.html', context)

def blog_detail(request, post_slug):
    post = get_object_or_404(Post.objects.prefetch_related('content_blocks'), slug=post_slug, is_published=True)
    return render(request, 'blog_detail.html', {'post': post})

def about_detail(request):
    about_page = AboutPage.objects.first()
    return render(request, 'about_detail.html', {'about_page': about_page})

def video_list(request):
    videos_list = Video.objects.select_related('category').filter(is_published=True).order_by('-published_date')
    categories = VideoCategory.objects.all()
    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        videos_list = videos_list.filter(category__slug=category_slug)
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    has_featured = Video.objects.filter(is_published=True, is_featured=True).exists()
    paginator = Paginator(videos_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'videos': page_obj,
        'categories': categories,
        'active_category': category_slug,
        'has_featured': has_featured,
    }
    return render(request, 'video_list.html', context)

def video_list_partial(request):
    if not request.headers.get('HX-Request'):
        return redirect(f"{reverse('video_list')}?{request.META['QUERY_STRING']}")

    videos_list = Video.objects.select_related('category').filter(is_published=True).order_by('-published_date')
    category_slug = request.GET.get('category')
    featured = request.GET.get('featured')

    if category_slug:
        videos_list = videos_list.filter(category__slug=category_slug)
    if featured:
        videos_list = videos_list.filter(is_featured=True)

    paginator = Paginator(videos_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    has_featured = Video.objects.filter(is_published=True, is_featured=True).exists()

    context = {
        'videos': page_obj,
        'categories': VideoCategory.objects.all(),
        'active_category': category_slug,
        'has_featured': has_featured,
    }
    return render(request, 'partials/video_list_content.html', context)

def video_detail(request, video_slug):
    video = get_object_or_404(Video, slug=video_slug, is_published=True)
    return render(request, 'video_detail.html', {'video': video})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, message]):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        async_send_contact_email(name, email, message, settings.DEFAULT_FROM_EMAIL, settings.CONTACT_EMAIL)
        return JsonResponse({'success': True, 'message': 'Message queued successfully!'})
    return render(request, 'index.html')

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'message': 'Valid email required.'}, status=400)
        
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        if created:
            async_send_subscription_email(email, settings.DEFAULT_FROM_EMAIL)
            return JsonResponse({'success': True, 'message': 'Subscription successful!'})
        return JsonResponse({'success': True, 'message': 'You are already subscribed!'})