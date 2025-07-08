from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms import inlineformset_factory 
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
import logging

from .models import Post, Category, Tag, AboutPage, ContentBlock, Video, VideoCategory, Subscriber
from .forms import PostForm, CategoryForm, TagForm, AboutPageForm, ContentBlockForm, VideoForm, VideoCategoryForm

logger = logging.getLogger(__name__)

# IMPROVEMENT: Function now accepts the request object to build the URL dynamically
def _send_notification_emails(request, post):
    """
    Helper function to send notification emails to all subscribers.
    Returns True on success, False on failure.
    """
    subscribers = Subscriber.objects.all()
    recipient_list = [s.email for s in subscribers]

    if recipient_list:
        subject = f"New Blog Post: {post.title}"
        
        # IMPROVEMENT: Build the absolute URL dynamically from the request
        post_url = request.build_absolute_uri(post.get_absolute_url())

        message = (
            f"Hi there!\n\nA new post \"{post.title}\" has just been published.\n\n"
            f"Read it here: {post_url}\n\nStay tuned for more!"
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=['no-reply@yourdomain.com'],  # Dummy "To" field
                bcc=recipient_list,              # Real subscribers here
            )
            email.send(fail_silently=False)
            logger.info(f"Successfully sent notification for post '{post.title}' to {len(recipient_list)} subscribers.")
            return True
        except Exception as e:
            logger.error(f"Failed to send post notification emails for post '{post.title}': {str(e)}")
            return False
    return False


@login_required
def admin_dashboard(request):
    context = {
        'active_tab': 'dashboard',
        'post_count': Post.objects.count(),
        'category_count': Category.objects.count(),
        'tag_count': Tag.objects.count(),
        'recent_posts': Post.objects.all()[:5]
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'active_tab': 'posts',
        'posts': posts
    }
    return render(request, 'admin/posts.html', context)


@login_required
def admin_post_create(request):
    ContentBlockFormSet = inlineformset_factory(Post, ContentBlock, form=ContentBlockForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # We pass an empty Post instance to the formset
        formset = ContentBlockFormSet(request.POST, request.FILES, instance=Post())
        if form.is_valid() and formset.is_valid():
            post = form.save()
            formset.instance = post
            formset.save()

            # Check if the notification checkbox was checked
            send_to_subscribers = form.cleaned_data.get('send_to_subscribers')
            if send_to_subscribers and post.is_published:
                # IMPROVEMENT: Pass the request object to the helper function
                if _send_notification_emails(request, post):
                    post.notification_sent_at = timezone.now()
                    post.save(update_fields=['notification_sent_at'])

            return redirect('admin_posts')
    else:
        form = PostForm()
        formset = ContentBlockFormSet(instance=Post())
    
    context = {
        'active_tab': 'posts',
        'form': form,
        'formset': formset,
        'title': 'Create New Post'
    }
    return render(request, 'admin/post_form.html', context)


@login_required
def admin_post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ContentBlockFormSet = inlineformset_factory(Post, ContentBlock, form=ContentBlockForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        formset = ContentBlockFormSet(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            post = form.save()
            formset.instance = post
            formset.save()

            # Check if the notification checkbox was checked
            send_to_subscribers = form.cleaned_data.get('send_to_subscribers')
            # Only send if requested, the post is published, and it hasn't been sent before
            if send_to_subscribers and post.is_published and not post.notification_sent_at:
                # IMPROVEMENT: Pass the request object to the helper function
                if _send_notification_emails(request, post):
                    post.notification_sent_at = timezone.now()
                    post.save(update_fields=['notification_sent_at'])
            
            return redirect('admin_posts')
    else:
        form = PostForm(instance=post)
        formset = ContentBlockFormSet(instance=post)
    
    context = {
        'active_tab': 'posts',
        'form': form,
        'formset': formset, 
        'title': 'Edit Post',
        'post': post
    }
    return render(request, 'admin/post_form.html', context)

# ... (rest of the file is unchanged) ...
@login_required
def admin_post_delete(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def admin_categories(request):
    categories = Category.objects.all()
    context = {
        'active_tab': 'categories',
        'categories': categories
    }
    return render(request, 'admin/categories.html', context)

@login_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    context = {
        'active_tab': 'categories',
        'form': form,
        'title': 'Create New Category'
    }
    return render(request, 'admin/category_form.html', context)

@login_required
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'active_tab': 'categories',
        'form': form,
        'title': 'Edit Category',
        'category': category
    }
    return render(request, 'admin/category_form.html', context)

@login_required
def admin_category_delete(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def admin_tags(request):
    tags = Tag.objects.all()
    context = {
        'active_tab': 'tags',
        'tags': tags
    }
    return render(request, 'admin/tags.html', context)

@login_required
def admin_tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_tags')
    else:
        form = TagForm()
    
    context = {
        'active_tab': 'tags',
        'form': form,
        'title': 'Create New Tag'
    }
    return render(request, 'admin/tag_form.html', context)

@login_required
def admin_tag_edit(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('admin_tags')
    else:
        form = TagForm(instance=tag)
    
    context = {
        'active_tab': 'tags',
        'form': form,
        'title': 'Edit Tag',
        'tag': tag
    }
    return render(request, 'admin/tag_form.html', context)

@login_required
def admin_tag_delete(request, tag_id):
    if request.method == 'POST':
        tag = get_object_or_404(Tag, id=tag_id)
        tag.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def admin_about(request):
    about_page = AboutPage.objects.first()
    
    if request.method == 'POST':
        form = AboutPageForm(request.POST, request.FILES, instance=about_page)
        if form.is_valid():
            form.save()
            return redirect('admin_about')
    else:
        form = AboutPageForm(instance=about_page)
    
    context = {
        'active_tab': 'about',
        'form': form,
        'title': 'Edit About Page'
    }
    return render(request, 'admin/about_form.html', context)


@login_required
def admin_videos(request):
    videos = Video.objects.all()
    context = {
        'active_tab': 'videos',
        'videos': videos
    }
    return render(request, 'admin/videos.html', context)

@login_required
def admin_video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_videos')
    else:
        form = VideoForm()

    context = {
        'active_tab': 'videos',
        'form': form,
        'title': 'Add New Video'
    }
    return render(request, 'admin/video_form.html', context)


@login_required
def admin_video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('admin_videos')
    else:
        form = VideoForm(instance=video)

    context = {
        'active_tab': 'videos',
        'form': form,
        'title': 'Edit Video',
        'video': video
    }
    return render(request, 'admin/video_form.html', context)

@login_required
def admin_video_delete(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# ++ Add views for Video Category management ++


@login_required
def admin_video_categories(request):
    categories = VideoCategory.objects.all()
    context = {
        # Change active_tab to be specific to this page
        'active_tab': 'video_categories',
        'categories': categories
    }
    return render(request, 'admin/video_categories.html', context)

@login_required
def admin_video_category_create(request):
    if request.method == 'POST':
        form = VideoCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_video_categories')
    else:
        form = VideoCategoryForm()
    
    context = {
        # Also update here
        'active_tab': 'video_categories',
        'form': form,
        'title': 'Create New Video Category'
    }
    return render(request, 'admin/video_category_form.html', context)


@login_required
def admin_video_category_edit(request, category_id):
    category = get_object_or_404(VideoCategory, id=category_id)
    if request.method == 'POST':
        form = VideoCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_video_categories')
    else:
        form = VideoCategoryForm(instance=category)
    
    context = {
        'active_tab': 'video_categories',
        'form': form,
        'title': 'Edit Video Category',
        'category': category
    }
    return render(request, 'admin/video_category_form.html', context)

@login_required
def admin_video_category_delete(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(VideoCategory, id=category_id)
        try:
            category.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            # This can fail if there are videos still linked to this category
            # depending on the on_delete policy.
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})