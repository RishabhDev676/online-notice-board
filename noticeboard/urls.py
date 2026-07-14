from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Django default admin (we will NOT use it publicly)
    path('dj-admin/', admin.site.urls),

    # Admin panel (custom)
    path('admin/', include('accounts.urls')),

    # Public notice pages
    path('', include('notices.urls')),

    # Email subscriptions
    path('subscriptions/', include('subscriptions.urls')),
]

# Media files (PDFs) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
