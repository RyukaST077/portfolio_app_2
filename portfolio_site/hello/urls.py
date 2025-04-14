from django.urls import path

from .views import index, page_top

urlpatterns = [
    path("", index, name="index"),
    path("top", page_top, name="page_top")
]