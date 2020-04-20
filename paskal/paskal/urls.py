from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('user.urls', 'user'), namespace='user')),
    path('action/', include(('action.urls', 'action'), namespace='action')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = 'paskal.views.permission_denied'
