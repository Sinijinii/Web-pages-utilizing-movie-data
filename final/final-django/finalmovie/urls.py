from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('movies.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/saveinfo/', views.saveinfo)
    path('articles/', include('articles.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
