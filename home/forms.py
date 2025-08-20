from django import forms
from .models import Post, Category, Tag, AboutPage, ContentBlock, Video, VideoCategory

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
        # Ensure 'slug' is included if you want it to be editable in the form
        fields = ['title', 'slug', 'excerpt', 'image', 'category', 'tags', 'is_published', 'send_to_subscribers']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2'})
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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

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
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'slug', 'description', 'video_url', 'thumbnail', 'category', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }