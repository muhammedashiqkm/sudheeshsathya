from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # Change 'home' to your main app name
]

# This line allows Django to serve images in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)