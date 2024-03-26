from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, SettingsForm
from .models import *
from django.db.models import F
from django.apps import apps
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.utils.http import urlencode



# Create your views here.
def index(request):
    """
    returns the home page
    """
    return render(request, "main/index.html")


def search_page(request):

    form = SearchForm(request.GET)
    if form.is_valid():
        # get model results based off get params
        search_model = request.GET.get('model')                  # gets from the url the model specified
        search_query = request.GET.get('query')                     # gets from the url the search query

        model_obj = apps.get_model('main', search_model)
        search_results = model_obj.search_db(model_obj, "name", search_query)

        # create paginator to manage the multiple pages of results
        paginator = Paginator(search_results, 10)                    # paginator class from django show 2 results of the model output
        page_number = request.GET.get("page", 1)                    # get the current page of results or 1 if none
        page_obj = paginator.get_page(page_number)                  # paginator returns the page data

        # render page (added params to keep search paramaters through the different pages.
        return render(request, "main/search_page.html", {"page_obj": page_obj, "model": search_model, "params":urlencode({"model":search_model, "query":search_query})})
    else:
        return render(request, "main/search_page.html")

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
