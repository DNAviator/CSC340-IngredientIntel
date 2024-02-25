from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    returns the home page
    """
    return render(request, "main/index.html")

def search_page(request, query):
    """
    returns the page of search results
    """
    context = {"result_names":["sugar", "aspertame", "stevia"]}

    return render(request, "main/search_page.html", context)

def results_page(request, type, object):
    """
    returns the page describing the item, company, or product
    """
    context = {"type": type, "object": object}

    return render(request, "main/results_page.html", context)
