# home/forms.py

from django import forms
from .models import Post, PostCategory, ContentBlock, AboutPage, Video, VideoCategory, Subscriber

class PostForm(forms.ModelForm):
    """
    Custom form for the Post model to include the notification checkbox.
    """
    send_to_subscribers = forms.BooleanField(
        required=False,
        label="Send notification to all subscribers",
        help_text="Queues an email for all active subscribers when the post is saved as 'Published'."
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'image', 'category', 'is_published', 'is_featured', 'send_to_subscribers']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Disables the notification checkbox if a notification has already been sent.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.notification_sent_at:
            self.fields['send_to_subscribers'].disabled = True
            self.fields['send_to_subscribers'].help_text = f"A notification was already sent on {self.instance.notification_sent_at.strftime('%Y-%m-%d %H:%M')}."

class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ['block_type', 'content', 'image', 'caption', 'order']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 8ch;'}),
        }

class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ['title', 'subtitle', 'content', 'profile_image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'rich-text-editor'}),
            'subtitle': forms.Textarea(attrs={'rows': 2}),
        }

class VideoCategoryForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class VideoForm(forms.ModelForm):
    
    # --- NEW: Added notification checkbox ---
    send_to_subscribers = forms.BooleanField(
        required=False,
        label="Send notification to all subscribers",
        help_text="Queues an email for all active subscribers when the video is saved as 'Published'."
    )
    # ----------------------------------------

    class Meta:
        model = Video
        # UPDATED: Added 'send_to_subscribers' to fields
        fields = [
            'title', 'slug', 'excerpt', 'description', 'video_url', 
            'thumbnail', 'category', 'is_published', 'is_featured', 
            'send_to_subscribers'
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    # --- NEW: Added __init__ to disable checkbox ---
    def __init__(self, *args, **kwargs):
        """
        Disables the notification checkbox if a notification has already been sent.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.notification_sent_at:
            self.fields['send_to_subscribers'].disabled = True
            self.fields['send_to_subscribers'].help_text = f"A notification was already sent on {self.instance.notification_sent_at.strftime('%Y-%m-%d %H:%M')}."
    # ----------------------------------------------