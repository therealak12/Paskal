from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('user.urls', 'user'), namespace='user')),
    path('action/', include(('action.urls', 'action'), namespace='action')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler403 = 'paskal.views.permission_denied'
handler404 = 'paskal.views.not_found'
