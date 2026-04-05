# home/tasks.py
import resend
import logging
from background_task import background
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import Post, Video, Subscriber 

logger = logging.getLogger(__name__)

@background(schedule=1)
def send_post_notification_email_task(post_id):
    """Broadcasts a new post alert to all active subscribers via Resend API."""
    resend.api_key = settings.RESEND_API_KEY
    try:
        post = Post.objects.get(id=post_id)
        if post.notification_sent_at:
            return f"Notification for '{post.title}' already sent."

        # Fetch active subscribers
        recipient_list = list(Subscriber.objects.filter(is_active=True).values_list('email', flat=True))

        if not recipient_list:
            return "No active subscribers found."

        post_url = f"{settings.SITE_DOMAIN}{reverse('blog_detail', args=[post.slug])}"
        
        # Use Resend API directly to bypass Railway's port blocks
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": recipient_list,
            "subject": f"New Blog Post: {post.title}",
            "html": f"<h3>{post.title}</h3><p>{post.excerpt}</p><a href='{post_url}'>Read More</a>"
        })

        post.notification_sent_at = timezone.now()
        post.save(update_fields=['notification_sent_at'])
        logger.info(f"Broadcasted post {post_id} to {len(recipient_list)} users.")

    except Exception as e:
        logger.error(f"Error in post notification: {e}")
        raise e

@background(schedule=1)
def send_video_notification_email_task(video_id):
    """Broadcasts a new video alert to all active subscribers via Resend API."""
    resend.api_key = settings.RESEND_API_KEY
    try:
        video = Video.objects.get(id=video_id)
        if video.notification_sent_at:
            return f"Notification for '{video.title}' already sent."

        recipient_list = list(Subscriber.objects.filter(is_active=True).values_list('email', flat=True))

        if not recipient_list:
            return "No active subscribers found."

        video_url = f"{settings.SITE_DOMAIN}{reverse('video_detail', args=[video.slug])}"
        
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": recipient_list,
            "subject": f"New Video: {video.title}",
            "html": f"<h3>{video.title}</h3><p>{video.excerpt}</p><a href='{video_url}'>Watch Now</a>"
        })

        video.notification_sent_at = timezone.now()
        video.save(update_fields=['notification_sent_at'])
        logger.info(f"Broadcasted video {video_id} to {len(recipient_list)} users.")

    except Exception as e:
        logger.error(f"Error in video notification: {e}")
        raise e