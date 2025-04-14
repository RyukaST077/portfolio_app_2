from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "hello/index.html")

def page_top(request):
    return render(request, "hello/top.html")

def page_about(request):
    return render(request, "hello/about.html")

def page_contact(request):
    return render(request, "hello/contact.html")

def page_portfolio(request):
    return render(request, "hello/portfolio.html")