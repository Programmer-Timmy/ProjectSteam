from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', {'page_title': 'Home', 'show_footer': False})


