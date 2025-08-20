# myapp/tasks.py

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import Post, Subscriber

@shared_task
def send_post_notification_email_task(post_id):
    """
    Celery task to send notification emails for a newly published post.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return f"Post with id {post_id} not found."

    # Mark the notification as sent immediately to prevent race conditions
    post.notification_sent_at = timezone.now()
    post.save(update_fields=['notification_sent_at'])

    subscribers = Subscriber.objects.filter(is_active=True) # Assuming you add an 'is_active' field
    recipient_list = [s.email for s in subscribers]

    if not recipient_list:
        return f"No active subscribers found for post '{post.title}'."

    subject = f"New Blog Post: {post.title}"
    post_url = f"{settings.SITE_DOMAIN}{reverse('blog_detail', args=[post.slug])}"
    
    message = (
        f"Hi there!\n\nA new post \"{post.title}\" has been published.\n\n"
        f"Read it here: {post_url}\n\nStay tuned!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        email = EmailMessage(
            subject=subject, body=message, from_email=from_email, to=['no-reply@yourdomain.com'], bcc=recipient_list
        )
        email.send(fail_silently=False)
        return f"Successfully sent notification for post '{post.title}' to {len(recipient_list)} subscribers."
    except Exception as e:
        return f"Failed to send emails for post '{post.title}': {str(e)}"