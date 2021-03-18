from django.shortcuts import render
from django.http import HttpResponse

from . import models


# Create your views here.
def gpio(request):
    return HttpResponse('GPIO OUTPUT!')


def display_HubData(request):
    data = models.HubData.objects.all()  # Collect all records from table
    return render(request, 'data.html', {'data': data, 'name': 'Hub-Data'})


def display_HubCache(request):
    data = models.HubCache.objects.all()  # Collect all records from table
    return render(request, 'data.html', {'data': data, 'name': 'Cache-Data'})
