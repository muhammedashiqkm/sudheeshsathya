# home/admin.py

from django.contrib import admin
from .models import PostCategory, Post, ContentBlock, VideoCategory, Video, AboutPage, Subscriber
from .forms import PostCategoryForm, PostForm, ContentBlockForm, VideoCategoryForm, VideoForm, AboutPageForm

# --- UPDATED: Import the tasks ---
from .tasks import send_post_notification_email_task, send_video_notification_email_task

# --- Inlines ---

class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    form = ContentBlockForm
    extra = 1
    fields = ('order', 'block_type', 'content', 'image', 'caption')
    ordering = ('order',)

# --- ModelAdmins ---

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    form = PostCategoryForm
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'category', 'is_published', 'is_featured', 'published_date', 'notification_sent_at')
    list_filter = ('is_published', 'is_featured', 'category', 'published_date')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    inlines = [ContentBlockInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'image', 'category')
        }),
        ('Status & Visibility', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Subscriber Notification', {
            'fields': ('send_to_subscribers',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # 1. Save the object first
        super().save_model(request, obj, form, change)
        
        # 2. Check if the notification should be sent
        send_notification = form.cleaned_data.get('send_to_subscribers')
        
        if (send_notification and 
            obj.is_published and 
            not obj.notification_sent_at):
            
            # 3. Call the task directly (no .delay())
            send_post_notification_email_task(obj.id)

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    form = VideoCategoryForm
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ('title', 'category', 'is_published', 'is_featured', 'published_date', 'notification_sent_at')
    list_filter = ('is_published', 'is_featured', 'category', 'published_date')
    search_fields = ('title', 'excerpt', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'video_url', 'thumbnail')
        }),
        ('Content', {
            'fields': ('excerpt', 'description')
        }),
        ('Status & Visibility', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Subscriber Notification', {
            'fields': ('send_to_subscribers',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # 1. Save the object first
        super().save_model(request, obj, form, change)
        
        # 2. Check if the notification should be sent
        send_notification = form.cleaned_data.get('send_to_subscribers')
        
        if (send_notification and 
            obj.is_published and 
            not obj.notification_sent_at):
            
            # 3. Call the task directly (no .delay())
            send_video_notification_email_task(obj.id)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    form = AboutPageForm
    
    def has_add_permission(self, request):
        return AboutPage.objects.count() == 0

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)