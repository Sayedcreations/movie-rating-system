from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls'),),
    path('pro/',include('filim_pro.urls',namespace='film_pro'),),
    path('user/',include('filim_user.urls',namespace='film_user'),),
    path('site-admin/',include('site_admin.urls',namespace='site_admin'),)
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
