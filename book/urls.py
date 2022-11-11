
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('main_page.urls')),
    path('profile/', include('userprofiles.urls')),
    path('admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    path('items/',include('items.urls')),
    path('auth/',include('loginsys.urls')),
    path('search/',include('searchsys.urls')),
    path('library/',include('library.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
