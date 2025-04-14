from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "hello/index.html")

def page_top(request):
    return render(request, "hello/top.html")