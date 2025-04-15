from django.urls import path

from .views import index, page_top, page_about, page_contact, page_portfolio
app_name = 'hello' # 名前空間を設定

urlpatterns = [
    path("", index, name="index"),
    path("top", page_top, name="page_top"),
    path("about", page_about, name="page_about"),
    path("contact", page_contact, name="page_contact"),
    path("portfolio", page_portfolio, name="page_portfolio"),
]