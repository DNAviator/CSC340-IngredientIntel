from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import SearchForm, SettingsForm, BarcodeForm, ConsumerCreationForm, NewProductForm
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
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponseRedirect
import os
import cv2
from pyzbar.pyzbar import decode
from dal import autocomplete



class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    """
    Helper view that allows for an autocomplete select for the ingredients for product creation
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Ingredient.objects.none()

        qs = Ingredient.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

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
        paginator = Paginator(search_results, 2)                    # paginator class from django show 2 results of the model output
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
    info = model_to_dict(info)

    del info["id"]

    for key in info : # This for loop looks for unwanted formatting from the ManytoMany Field type and makes it look nicer to a user
        content = str(info[key])


        if content[0] == "[" :
            content = content[1:-1]
            content = content.replace(">", "")
            content = content.replace("<Ingredient: ", "")
            content = content.replace("<Product: ", "")

            info[key] = content

        

    context = {"type": type, "info": info}

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

def logout_page(request):
    logout(request)
    messages.success(request, ("Logged Out"))
    return redirect('home')

@login_required(redirect_field_name='login')
def settings(request):
    """
    Returns the setting page if the user is authenticated as a consumer
    """
    if not request.user.is_authenticated:
        messages.success(request, ("Login before accessing settings"))
        return redirect('login')

    # need to add functionality to view the current settings probably can show things easily
    # but need to figure out how to pull up editable form
    return render(request, "main/settings.html", {"settings":SettingsForm})

def sign_up(request):
    if request.method == "POST":
        form = ConsumerCreationForm(request.POST)  
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
    form = ConsumerCreationForm()  # generate form to pass as context
    return render(request, "main/sign_up.html", {"form":form}) # render the page with the form


def scan_barcode(request):      
    context = {}
    if request.method == "POST":
        form = BarcodeForm(request.POST, request.FILES)
        if form.is_valid(): 
            img = form.cleaned_data.get("image") # Stores image from form 
            
            
            obj = ImageModel.objects.create(img = img) # Creates an image model with an image as input
           
            image_url = obj.img.path # stores directory of the image


            barcode = cv2.imread(image_url)

            os.unlink(image_url) # Removes image from media/images

            decoded = decode(barcode) # Decodes barcode from a user's image
            if len(decoded) == 0: #If barcode has nothing it points to, redirect to scan_barcode
                return redirect('scan_barcode')
            if str(decoded[0].type) == "QRCODE":
                return redirect('scan_barcode')
            upc = str(decoded[0].data)
            upc = upc[2:-1] # Removes unwanted formatting on upc number
            
            try:
                item = Product.objects.get(item_id=upc) # Scans DB for a product with the same upc as the one in a user's image
            except ObjectDoesNotExist :
                return redirect('scan_barcode')
            
            
            return redirect('result_page', "Product", item.id) # Sends users to correct item

    else:
        form = BarcodeForm()
    context['form']= form
    return render(request, "main/scan_barcode.html", context)


@login_required(redirect_field_name='researcher_login')
def researcher(request):
    return render(request, "main/researcher.html")

@login_required(redirect_field_name='company_login')
def company(request):
    company_object=Company.objects.get(name="Test")

    if request.method == "POST":
        form = NewProductForm(request.POST) # this is a hack needs to be fixed
        if form.is_valid(): 
            form.save()
            messages.success(request, ("Product Successfuly Created"))
            return redirect('company')
        else:
            messages.success(request, ("Error Creating Product"))
            return redirect('company')
    form = NewProductForm() # this needs to be fixed
    company = request.user
    products = Product.objects.filter(producing_company=company_object) # get all the products this user has created
    return render(request, "main/company.html", {'form':form, 'products':products})

def about(request):
    return render(request, "main/about.html")
