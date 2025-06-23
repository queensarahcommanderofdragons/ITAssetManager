from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
import io

def home(request):
    return render(request, "home.html")


def load_db_view(request):
    try:
        with open('db_utf16.json', 'rb') as f:
            raw_data = f.read()
        decoded_data = raw_data.decode('utf-16')
        stream = io.StringIO(decoded_data)
        stream.name = 'db_utf16.json'  # Django uses this to infer format
        call_command('loaddata', stream)
        return HttpResponse(" Data loaded successfully into PostgreSQL.")
    except Exception as e:
        return HttpResponse(f" Error: {e}")

