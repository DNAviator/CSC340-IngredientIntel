from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    returns the home page
    """
    return HttpResponse("hi")

def search_page(request, query):
    """
    returns the page of search results
    """
    return HttpResponse(query)

def result_page(request, type, object):
    """
    returns the page describing the item, company, or product
    """
    return HttpResponse(f"type={type}, object={object}")
