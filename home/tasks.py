# home/tasks.py

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import Post, Video, Subscriber 

# Add retry logic to the task decorator
@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def send_post_notification_email_task(post_id):
    """
    Celery task to send notification emails for a newly published post.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return f"Post with id {post_id} not found."

    # Check the flag first to avoid re-sending if a retry happens
    if post.notification_sent_at:
        return f"Notification for post '{post.title}' was already sent."

    post.notification_sent_at = timezone.now()
    post.save(update_fields=['notification_sent_at'])

    subscribers = Subscriber.objects.filter(is_active=True)
    recipient_list = [s.email for s in subscribers]

    if not recipient_list:
        return f"No active subscribers found for post '{post.title}'."

    subject = f"New Blog Post: {post.title}"
    post_url = f"{settings.SITE_DOMAIN}{reverse('blog_detail', args=[post.slug])}"
    
    message = (
        f"Hi there!\n\nA new post \"{post.title}\" has been published.\n\n"
        f"Read it here: {post_url}\n\n"
        f"Read the excerpt:\n{post.excerpt}\n\nStay tuned!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = EmailMessage(
            subject=subject, body=message, from_email=from_email, to=['no-reply@yourdomain.com'], bcc=recipient_list
        )
        email.send(fail_silently=False)
        return f"Successfully sent notification for post '{post.title}' to {len(recipient_list)} subscribers."
    except Exception as e:
        # Re-raise the exception to trigger Celery's retry mechanism
        raise e


# Add retry logic to the task decorator
@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def send_video_notification_email_task(video_id):
    """
    Celery task to send notification emails for a newly published video.
    """
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return f"Video with id {video_id} not found."

    # Check the flag first to avoid re-sending if a retry happens
    if video.notification_sent_at:
        return f"Notification for video '{video.title}' was already sent."

    video.notification_sent_at = timezone.now()
    video.save(update_fields=['notification_sent_at'])

    subscribers = Subscriber.objects.filter(is_active=True)
    recipient_list = [s.email for s in subscribers]

    if not recipient_list:
        return f"No active subscribers found for video '{video.title}'."

    subject = f"New Video Published: {video.title}"
    video_url = f"{settings.SITE_DOMAIN}{reverse('video_detail', args=[video.slug])}"
    
    message = (
        f"Hi there!\n\nA new video \"{video.title}\" has been published.\n\n"
        f"Watch it here: {video_url}\n\n"
        f"About the video:\n{video.excerpt}\n\nStay tuned!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = EmailMessage(
            subject=subject, body=message, from_email=from_email, to=['no-reply@yourdomain.com'], bcc=recipient_list
        )
        
        # --- THE FIX IS HERE ---
        email.send(fail_silently=False)
        # -----------------------
        
        return f"Successfully sent notification for video '{video.title}' to {len(recipient_list)} subscribers."
    except Exception as e:
        # Re-raise the exception to trigger Celery's retry mechanism
        raise e