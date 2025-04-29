from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from writer_app import views as writer_views # signupビューをインポートするため


urlpatterns = [
    path("", include("hello.urls")),
    path("qrcode/", include("qrcode_app.urls")),
    path("writer/", include("writer_app.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', writer_views.signup, name='signup'),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

