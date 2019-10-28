# from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """Test index"""
    return HttpResponse('Hello World!')
