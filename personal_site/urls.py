# personal_site/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('', include('home.urls')), 
]

# When DEBUG=False, Django won't serve media. This forces it to serve 
# uploaded files out of the Railway Volume in production.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)