from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def say_hello(request):
    return HttpResponse('Hello, Alx World!')