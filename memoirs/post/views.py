from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from .models import Post




def index(request):
    return render(request, 'post/index.html')


