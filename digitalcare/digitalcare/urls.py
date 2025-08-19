from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.generic import TemplateView

# main urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    
   # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # re_path('', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

