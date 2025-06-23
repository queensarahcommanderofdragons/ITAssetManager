from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

