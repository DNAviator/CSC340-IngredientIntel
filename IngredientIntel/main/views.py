from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, SettingsForm
from .models import *
from django.db.models import F
from django.apps import apps

# general search function (currently causing an error)
def search_db(model, query, page=1):

        modelFromStr = apps.get_model('main', model)
        # ranks all results with Levenshtein distance function to query
        result = modelFromStr.objects.annotate(
            rank= Levenshtein(modelFromStr.name, query)
        ).order_by('rank')

        # page number used to generate the set of results to see
        startIndex = 25 * (page - 1)
        
        # checks if indexes are in bounds and returns best array slice
        if startIndex > result.count():
            return []
        elif startIndex + 25 > result.count():
            return result[startIndex:len(result)-1]
        
        return result[startIndex:startIndex+25]


# Create your views here.
def index(request):
    """
    returns the home page
    """
    return render(request, "main/index.html")

def search_page(request, page=1):
    """
    returns the page of search results
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_criteria = form.cleaned_data['search_criteria']
            search_query = form.cleaned_data['search_query']

            search_results = search_db(search_criteria, search_query, page)

            # Process search logic based on criteria and query
            context = {"results":search_results, "type":search_criteria, "query":search_query}
            return render(request, "main/search_page.html", context)
        
    # if there is an invalid input returns the no results page
    return render(request, "main/search_page.html", {"results": False})

def results_page(request, type, id):
    """
    returns the page describing the item, company, or product
    """
    #hardcoded info
    info = {
        "name":"Sugar",
        "purpose":"To sweeten product",
        "warnings":"May cause hyperglycemia and increase heart rate",
        "notes":"Research articles: [link1, link2, link3]",
        "num_products":100000,
    }
    context = {"type": type, "info": info}

    return render(request, "main/results_page.html", context)

def login(request):
    """
    Runs the login page
    """
    return render(request, "main/login.html")

def settings(request):
    return render(request, "main/settings.html", {"settings":SettingsForm})

def sign_up(request):
    return render(request, "main/sign_up.html")

def scan_barcode(request):
    return render(request, "main/scan_barcode.html")
def researcher(request):
    return render(request, "main/researcher.html")

def company(request):
    
    return render(request, "main/company.html")

def about(request):
    return render(request, "main/about.html")
