from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm

# Create your views here.
def index(request):
    """
    returns the home page
    """
    context = {"form":SearchForm}
    return render(request, "main/index.html", context)

def search_page(request):
    """
    returns the page of search results
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_criteria = form.cleaned_data['search_criteria']
            search_query = form.cleaned_data['search_query']

            # Process search logic based on criteria and query
            context = {"result_names":["sugar", "aspertame", "stevia"], "Type":search_criteria, "query":search_query, "no_results": False}
            return render(request, "main/search_page.html", context)
    # if there is an invalid input returns the no results page
    return render(request, "main/search_page.html", {"no_results": True})

def results_page(request, type, object):
    """
    returns the page describing the item, company, or product
    """
    context = {"type": type, "object": object}

    return render(request, "main/results_page.html", context)

def login(request):
    """
    Runs the login page
    """
    return render(request, "main/login.html")