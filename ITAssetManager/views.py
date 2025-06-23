from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
import io

def home(request):
    return render(request, "home.html")

def load_db_view(request):
    try:
        call_command('loaddata', 'db_utf16.json', format='json')
        return HttpResponse("✅ Data loaded successfully into PostgreSQL.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")