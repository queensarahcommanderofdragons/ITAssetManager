from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
import io

def home(request):
    return render(request, "home.html")

def load_db_view(request):
    try:
        with open('db_utf16.json', 'r', encoding='utf-16') as f:
            data = f.read()
        stream = io.StringIO(data)
        stream.name = 'db_utf16.json'
        call_command('loaddata', stream)
        return HttpResponse("Data loaded successfully into PostgreSQL.")
    except Exception as e:
        return HttpResponse(f" Error: {e}")