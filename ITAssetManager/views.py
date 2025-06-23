from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def load_db_view(request):
    try:
        call_command('loaddata', 'db.json')
        return HttpResponse("Data loaded successfully into PostgreSQL.")
    except Exception as e:
        return HttpResponse(f" Error: {e}")