from django.urls import path
from . import views
app_name = 'writer_app' # 名前空間を設定

urlpatterns = [
    path("", views.index, name="index"),
    path('api-key/', views.manage_api_key, name='manage_api_key'),
    path('ask/', views.ask_gemini, name='ask_gemini'),
]