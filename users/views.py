from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def say_hello(request):
    x=1
    return HttpResponse('Hello, Alx World!')