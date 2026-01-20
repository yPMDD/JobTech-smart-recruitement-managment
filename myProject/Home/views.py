from django.shortcuts import render


# Create your views here.

def homepage(req):
    return render(req,'index.html')

def about(req):
    return render(req,'about.html')