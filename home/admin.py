from django.contrib import admin, messages
from django.utils import timezone
from .models import Category, Post, Tag, ContentBlock, VideoCategory, Video, AboutPage, Subscriber
from .forms import PostForm
from .tasks import send_post_notification_email_task

class ContentBlockInline(admin.TabularInline):
    """
    Allows editing ContentBlocks directly within the Post admin page.
    """
    model = ContentBlock
    extra = 1
    fields = ('order', 'block_type', 'content', 'image', 'caption')
    ordering = ('order',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Use our custom form to get the notification checkbox in the admin
    form = PostForm

    list_display = ('title', 'category', 'is_published', 'notification_sent_at', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'notification_sent_at')
    date_hierarchy = 'created_at'
    inlines = [ContentBlockInline]

    def save_model(self, request, obj, form, change):
        """
        Overrides the save method to trigger the notification task.
        """
        # Save the object first
        super().save_model(request, obj, form, change)

        # Check the form's data for our custom field
        send_to_subscribers = form.cleaned_data.get('send_to_subscribers')

        # Trigger the task only if the box was checked and the post is published
        if send_to_subscribers and obj.is_published:
            send_post_notification_email_task.delay(obj.id)
            self.message_user(request, f"Notification for '{obj.title}' has been queued for sending.", messages.INFO)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'published_date')
    list_filter = ('is_featured', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_date', 'updated_at')

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Prevent adding more than one AboutPage
        return AboutPage.objects.count() == 0

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    list_editable = ('is_active',)

    def has_add_permission(self, request):
        # Subscribers should only be added via the public site form
        return False