from django import forms
from .models import Post, Category, Tag, AboutPage, ContentBlock, Video, VideoCategory

class PostForm(forms.ModelForm):
    send_to_subscribers = forms.BooleanField(
        required=False, 
        label="Send notification to all subscribers",
        help_text="Check this to send an email notification to all subscribers upon saving."
    )
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'image', 'category', 'tags', 'is_published', 'send_to_subscribers']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2'})
        }

# Form for the ContentBlock model
class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ['block_type', 'content', 'image', 'caption', 'order']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            # UPDATE: Change HiddenInput to NumberInput for the 'order' field
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