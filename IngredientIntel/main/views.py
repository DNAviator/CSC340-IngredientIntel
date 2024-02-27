from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, SettingsForm

# Create your views here.
def index(request):
    """
    returns the home page
    """
    return render(request, "main/index.html")

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
            context = {"result_names":["sugar", "aspertame", "stevia"], "type":search_criteria, "query":search_query, "no_results": False}
            return render(request, "main/search_page.html", context)
    # if there is an invalid input returns the no results page
    return render(request, "main/search_page.html", {"no_results": True})

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

def researcher(request):
    return render(request, "main/researcher.html")

def company(request):
    return render(request, "main/company.html")