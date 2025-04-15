
from django.urls import path
from . import views

app_name = 'qrcode_app' # 名前空間を設定

urlpatterns = [
    path('', views.index, name='index'), # /image/
    path('generate/', views.generate_qrcode_ajax, name='generate_qrcode_ajax'), # /image/generate/
]