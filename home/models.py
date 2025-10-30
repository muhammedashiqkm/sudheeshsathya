from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class PostCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Post Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return f"{reverse('blog_list')}?category={self.slug}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(help_text="A short description of the post")
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_featured = models.BooleanField(default=False, help_text="Check to feature this post on the main blog page.", db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)
    
    notification_sent_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])

    def get_related_posts(self):
        """Get posts in the same category, excluding this post"""
        return Post.objects.filter(category=self.category, is_published=True).exclude(id=self.id)[:3]


class ContentBlock(models.Model):
    BLOCK_TYPE_CHOICES = (
        ('rich_text', 'Rich Text'),
        ('heading', 'Heading'),
        ('image', 'Image'),
    )
    
    post = models.ForeignKey(Post, related_name='content_blocks', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPE_CHOICES, default='rich_text')
    
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='content_blocks/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_block_type_display()} block for {self.post.title}"


class VideoCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Video Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('video_list') + f'?category={self.slug}'

        
class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="A unique slug for the video URL.")
    excerpt = models.TextField(blank=True, help_text="A short description of the video.")
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="URL to the video (YouTube, Vimeo, etc.)")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, related_name='videos')
    
    is_featured = models.BooleanField(default=False, help_text="Check to feature this video on the main page.", db_index=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, db_index=True)
    
    notification_sent_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('video_detail', args=[self.slug])

    def get_embed_url(self):
     url = self.video_url.strip()
     if 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
     elif 'youtube.com' in url and 'v=' in url:
        video_id = url.split('v=')[-1].split('&')[0].split('?')[0]
     else:
        return url
     video_id = video_id.split('?')[0].split('&')[0]
     return f"https://www.youtube-nocookie.com/embed/{video_id}"


class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"
    
    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email