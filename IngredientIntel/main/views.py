from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import SearchForm, SettingsForm, BarcodeForm
from .models import *
from django.db.models import F
from django.apps import apps
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.utils.http import urlencode
from .bar_decoder import barcode_decoder
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


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
    #Get the model from the type, get the exact item or return 404    
    model_obj = apps.get_model('main', type)
    info = get_object_or_404(model_obj, pk=id)
    context = {"type": type, "info": model_to_dict(info)}

    return render(request, "main/results_page.html", context)

def login_page(request):
    """
    Runs the login page
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, (f"Successfully logged in as {username}"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error with your login, please try again"))
            return redirect('login')
    else:
        return render(request, "main/login.html")

def settings(request):
    return render(request, "main/settings.html", {"settings":SettingsForm})

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()
            newUser = User.objects.get(username=form.cleaned_data['username']) # Get the user object just created
            consumer = Group.objects.get(name='consumer') # get the consumer group object
            consumer.user_set.add(newUser)  # add the new user to the consumer group
            messages.success(request, 'Account created successfully') # output successful login and redirect to the login
            return redirect('login')
        else:
            messages.success(request, ("Error processing request, please try again")) # if an invalid form is passed in output error message
            return redirect('sign_up')
    form = UserCreationForm()  # generate form to pass as context
    return render(request, "main/sign_up.html", {"form":form}) # render the page with the form

def scan_barcode(request):
    #added barcode form here
    return render(request, "main/scan_barcode.html", {"barcode":BarcodeForm})

def researcher(request):
    return render(request, "main/researcher.html")

def company(request):
    return render(request, "main/company.html")

def about(request):
    return render(request, "main/about.html")
