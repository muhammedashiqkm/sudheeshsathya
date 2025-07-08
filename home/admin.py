from django.contrib import admin
from .models import Category, Post, Tag, ContentBlock, VideoCategory, Video, AboutPage, Subscriber

# Inline admin for ContentBlocks to be edited within the Post admin page
class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    extra = 1 # Number of empty forms to display
    fields = ('order', 'block_type', 'content', 'image', 'caption')
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') #
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} #


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'is_published', 'created_at') #
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)} #
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'notification_sent_at')
    inlines = [ContentBlockInline] # Embed the ContentBlock editor


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') #
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} #


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
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    search_fields = ('email',)
    readonly_fields = ('email', 'subscribed_at')

    def has_add_permission(self, request):
        # Subscribers should be added via the public form, not the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Prevent editing of subscriber records
        return False