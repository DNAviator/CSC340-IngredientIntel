from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.db.models import F
from django.apps import apps
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.utils.http import urlencode
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
import requests
from datetime import date




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
    """
    returns a page that shows a list of items with similar names to the users input.
    """
    form = SearchForm(request.GET)
    if form.is_valid():
        # get model results based off get params
        search_model = request.GET.get('model')                  # gets from the url the model specified
        search_query = request.GET.get('query')                     # gets from the url the search query

        model_obj = apps.get_model('main', search_model)
        search_results = model_obj.search_db(model_obj, "name", search_query)

        # create paginator to manage the multiple pages of results
        paginator = Paginator(search_results, 25)                    # paginator class from django show 2 results of the model output
        page_number = request.GET.get("page", 1)                    # get the current page of results or 1 if none
        page_obj = paginator.get_page(page_number)                  # paginator returns the page data
        if request.user.is_authenticated:
            flagged_ingredients = Profile.objects.get(pk = request.user.id).flagged_ingredients.all()
            for item in page_obj:
                if (item.ingredients.all() & flagged_ingredients):
                    item.flag = True


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
    info_model = get_object_or_404(model_obj, pk=id)
    info = model_to_dict(info_model)
    user_flags = []
    del info["id"]
    if "registered_users" in info.keys(): # Delete dangerous field if it exists
        del info["registered_users"]
        info["products"] =  ", ".join([item.name for item in info["products"]])
        del info["company_registration_number"]

    if "ingredients" in info.keys():
        if request.user.is_authenticated:
            flagged_ingredients = Profile.objects.get(pk = request.user.id).flagged_ingredients.all()
            user_flags = info_model.ingredients.all() & flagged_ingredients
        info["ingredients"] = ", ".join([item.name for item in info["ingredients"]])
        info["producing_company"] = Company.objects.get(pk=info["producing_company"]).name


    context = {"type": type, "info": info, "user_flags":user_flags}

    return render(request, "main/results_page.html", context)

def settings_page(request):
    """
    Returns the setting page if the user is authenticated as a consumer
    """
    if not request.user.is_authenticated:
        messages.success(request, ("Login before accessing settings"))
        return redirect('login')

    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, ("Settings successfully updated!"))
        else:
            messages.success(request, ("There was a problem updating your settings please try again"))
    
    user_settings = Profile.objects.get_or_create(pk = request.user.id) # should be replaced since all users should have settings
    return render(request, "main/settings.html", {"form":SettingsForm(instance=user_settings[0])})

def login_page(request):
    """
    login_page(request):
        POST:
            gets username and password from post request and tries to log the user in outputting a message depending on the result
            and redirecting to login if it fails, home otherwise
        GET:
            returns the login page html where a user can enter their information to log in
    """
    if request.method == "POST":
        username = request.POST['username'] # get username from post
        password = request.POST['password'] # get password from post
        user = authenticate(request, username=username, password=password) # django auth attempt
        if user is not None:
            login(request, user) # actually log user in
            messages.success(request, (f"Successfully logged in as {username}")) # send success message to html
            return redirect('home') # redirect home
        else:
            messages.success(request, ("There was an error with your login, please try again"))
            return redirect('login')
    else:
        return render(request, "main/login.html")

def logout_page(request):
    """
    logout_page(request): logs out the user contained in the request if they exist and redirects to home (does not have a corresponding view)
    """
    logout(request)
    messages.success(request, ("Logged Out"))
    return redirect('home')

def sign_up(request):
    """
    sign_up(request):
        Redirects to home if the user is already logged in
        POST:
            Checks that the post request contains the information for a user and if so creates the user and redirects to login
            If there is an error in this process redirects back to signup and displays an error message
        GET:
            Returns the html for the sign_up page with the user creation form passed as context allowing users to enter information for their account
    """
    if request.user.is_authenticated:
        messages.success(request, ("You are already logged in!"))
        return redirect('home')

    if request.method == "POST":
        form = ConsumerCreationForm(request.POST)  
        if form.is_valid():                                                    # Check form is filled out properly
            form.save()                                                        # Add new user to database
            newUser = User.objects.get(username=form.cleaned_data['username']) # Get the user object just created
            consumer = Group.objects.get(name='consumer')                      # get the consumer group object
            consumer.user_set.add(newUser)                                     # add the new user to the consumer group
            messages.success(request, 'Account created successfully')          # output successful login and redirect to the login
            return redirect('login')
        else:
            messages.success(request, ("Error processing request, please try again")) # if an invalid form is passed in output error message
            return render(request, "main/sign_up.html", {"form":form})
    form = ConsumerCreationForm()  # generate form to pass as context
    return render(request, "main/sign_up.html", {"form":form}) # render the page with the form

def scan_barcode(request):      
    """
    displays a page that allows image input, which can be scanned for a barcode, which will then check if that barcode is in the database.
    """
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

def researcher_login(request):
    """
    returns a page that allows a researcher to sign in
    """
    # redirect to home if user is already logged in else return html
    if request.user.is_authenticated:
        messages.success(request, ("You are already logged in, logout before attempting to login"))
        redirect('home')
    if request.method == "POST":
        username = request.POST['username'] # get username from post
        password = request.POST['password'] # get password from post
        user = authenticate(request, username=username, password=password) # django auth attempt
        if user is not None:
            login(request, user) # actually log user in
            messages.success(request, (f"Successfully logged in as {username}")) # send success message to html
            return redirect('home') # redirect home
        else:
            messages.success(request, ("There was an error with your login, please try again"))
            return redirect('./')

    return render(request, "main/researcher_login.html")

def researcher(request):
    """
    returns a page that allows a researcher to add research to ingredients in our database
    """
    current_user = request.user
    if current_user.is_authenticated:
        if current_user.groups.filter(name = 'Researcher').exists():
            if request.method == "POST":
                form = SCInoteForm(request.POST, researcher=current_user) # initializes form with post request and foreign key

                if form.is_valid():
                    form.save() # Adds product to the database
                    messages.success(request, ("Scientific Note Successfuly Created")) # output sucess message
                    return redirect('./') #keeps user at same directory
                else:
                    messages.success(request, ("Error Creating Product"))
                    return redirect('./')
            
            notes = SCINote.objects.filter(researcher=current_user)
            form = SCInoteForm(researcher=current_user)

            return render(request, "main/researcher.html", {'notes':notes, 'form':form})
    
    messages.success(request, ('Please log into a research account'))
    return redirect('researcher_login') # maybe not the cleanest solution

def company(request, company):
    """
    returns a company page that allows companies to add, delete and modify products in the database
    """

    company_object=Company.objects.get(name=company)
    if company_object.registered_users.filter(pk=request.user.pk).exists():

        if request.method == "POST":
            form = NewProductForm(request.POST) # initializes form with post request and foreign key

            if form.is_valid():
                form.instance.producing_company = company_object
                form.save() # Adds product to the database
                messages.success(request, ("Product Successfuly Created")) # output sucess message
                return redirect('./') #keeps user at same directory
            else:
                messages.success(request, ("Error Creating Product"))
                return redirect('./')
        form = NewProductForm()
        products = Product.objects.filter(producing_company=company_object) # get all the products this user has created
        return render(request, "main/company.html", {'form':form, 'products':products, 'company_name':company})
    else:
        messages.success(request, ('Please log into a user account registered to this company...'))
        return redirect('login')

def update_item(request, model_type, item_id):
    """
    Not configured yet, designed to allow for the update of products, should redirect to the company page after submission sending the post request to be dealt with there
    """
    model = apps.get_model(app_label='main', model_name=model_type)
    item_object = model.objects.filter(id=item_id) # filter used to prevent crash
    if not item_object:
        messages.success(request, ('Critical Error item not found, please try again'))
        redirect('home')
    
    item_object = item_object[0] # converts it from queryset to actual item

    if model_type == "product":
        company_object = Company.objects.get(id=item_object.producing_company.id) # can't crash since field is required
        if company_object.registered_users.filter(pk=request.user.pk).exists():
            form = NewProductForm(instance=item_object) # create filled in form to pass to view
            return render(request, "main/update.html", {'form':form, 'model_type':model_type, 'item_id':item_id})
        
        messages.success(request, ("Access Denied, not in company"))
        return redirect('home')
    elif model_type == "sciNote":
        if request.user.id == item_object.researcher.id:
            form = SCInoteForm(instance=item_object, researcher=item_object.researcher.id) # create filled in form to pass to view
            return render(request, "main/update.html", {'form':form, 'model_type':model_type, 'item_id':item_id})
    else:
        messages.success(request, ('Critical Error, please try again'))
        redirect('home')

def delete_product(request, model_type, item_id): 
    """
    Allows deletion of products
    """

    model = apps.get_model(app_label='main', model_name=model_type)
    item_object = model.objects.filter(id=item_id)

    if not item_object:
        messages.success(request, ('Critical Error item not found, please try again'))
        redirect('home')

    item_object = item_object[0]
    if model_type == "product":
        company_object = Company.objects.get(id = item_object.producing_company.id) 
        
        if not company_object.registered_users.filter(pk=request.user.pk).exists():
            messages.success(request, ("Access Denied"))
            return redirect('home')
        
        item_object.delete()
        messages.success(request, ("Item Successfuly Deleted")) # output sucess message
        return redirect(f"/company/{company_object.name}/")
    
    elif model_type == "sciNote": # Check if the model is sciNote
        
        if item_object.researcher.id != request.user.id:# if the user is a researcher who created the sciNote, then allows the user to delete the sciNote, if not, the denies access
            messages.success(request, ("Access Denied"))
            return redirect('home')
        
        item_object.delete()
        messages.success(request, ("Item Successfuly Deleted")) # output sucess message

        return redirect('researcher')
    # catch all for things like invalid forms or get requests
    messages.success(request, ("Access Denied"))
    return redirect('home')

def update_backend(request, model_type, item_id):
    """
    Does backed work to update a product or sci note
    """
    if request.method == "POST":
        model = apps.get_model(app_label='main', model_name=model_type)
        item_object = model.objects.filter(id=item_id) # filter used to prevent crash
        if not item_object:
            messages.success(request, ('Critical Error item not found, please try again'))
            redirect('home')

        item_object = item_object[0] # converts it from queryset to actual item
        if model_type == "product":
            company_object = Company.objects.get(id = item_object.producing_company.id) # can't crash since field is required

            # if the user does not belong to the company break out before editing item
            if not company_object.registered_users.filter(pk=request.user.pk).exists():
                messages.success(request, ("Access Denied"))
                return redirect('home')
            
            form = NewProductForm(request.POST) # create filled in form to pass to view
            if form.is_valid():
                form.instance.producing_company = company_object.id
                item_object.delete()
                form.save()
                messages.success(request, ("Item Successfuly Updated")) # output sucess message
                return redirect(f"/company/{item_object.producing_company.name}")
            else:
                messages.success(request, ("Error Creating Product"))

        elif model_type == "sciNote":
            form = SCInoteForm(request.POST, researcher=request.user.id) # initializes form with post request and foreign key
            
            # if the researcher is not the one who created the note they are trying to update break out
            if item_object.researcher.id != request.user.id:
                messages.success(request, ("Access Denied"))
                return redirect('home')
            
            if form.is_valid():
                item_object.delete()
                form.save() # Adds product to the database
                messages.success(request, ("Scientific Note Successfuly Updated")) # output sucess message
                return redirect('researcher')
            else:
                messages.success(request, ("Error Creating Product"))

    # catch all for things like invalid forms or get requests
    messages.success(request, ("Access Denied"))
    return redirect('home')
                
def about(request):
    """
    returns the about page
    """
    return render(request, "main/about.html")

def create_company(request):
    """
    returns page that allows a company to create a company object in the database
    """
    if not request.user.is_authenticated:
        messages.success(request, ("Please Login First"))
        return redirect('login')

    if request.method == "POST":
        form = NewCompanyForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            new_item.registered_users.add(request.user.id)
            messages.success(request, ("Company Created Successfully"))
            return redirect('company', request.POST['name'])
        else:
            messages.success(request, ("Error with company creation please try again..."))
            return redirect('create_company')

    return render(request, "main/company_signup.html", {"form": NewCompanyForm})

def select_company(request):
    """
    returns the a page that allows a registered company user to choose what company they want to add products to.
    This only shows the companies they are registered for
    """
    # Get the current user and then do a reverse match on the related name of the registered user field of the company model
    if not request.user.is_authenticated:
        messages.success(request, ("Please Login First"))
        return redirect('login')

    current_user = request.user
    valid_companies = current_user.registered_users.all()
    return render(request, "main/company_select.html", {"valid_companies": valid_companies})

def researcher_signup(request):
    """
    returns a page that allows researchers to sign up
    """

    # if user is logged in redirect to home with appropriate message
    if request.user.is_authenticated:
        if request.user.group.filter(name='Researcher'):
            messages.success(request, ("You are already logged in!"))
        else:
            messages.success(request, ("Logout of personal account before creating research account"))
        return redirect('home')

    if request.method == "POST":
        form = ResearcherSignUpForm(request.POST)  
        if form.is_valid():                                                    
            form.save()                                                        
            newUser = User.objects.get(username=form.cleaned_data['username']) 
            researcher_group = Group.objects.get(name='Researcher')                      
            researcher_group.user_set.add(newUser)                                     
            messages.success(request, 'Account created successfully')         
            return redirect('login')
        else:
            messages.success(request, ("Error processing request, please try again"))
            return render(request, "main/researcher_signup.html", {"form":form})
    form = ResearcherSignUpForm() 
    return render(request, "main/researcher_signup.html", {"form":form}) 

def fetch_api_data(request):
    query = 'lays'  
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=EOcBurjhuDFV9xf0NhZtNgMxQhzZ2YTu4NqeZ0b6&query={query}'
    #url = 'https://api.nal.usda.gov/fdc/v1/food/1518547?api_key=EOcBurjhuDFV9xf0NhZtNgMxQhzZ2YTu4NqeZ0b6'
    response = requests.get(url).json()
    
    response = response['foods'] 
    print("hello")
    print(response[0]['gtinUpc'])

    #the attributes of a product
    product_name = response[0]['description']
    brandOwner = response[0]['brandOwner']
    upcId = response[0]['gtinUpc']
    #Finish attributes

    company = Company.objects.create(
    name=brandOwner,
    date_founded=date(year=2000, month=1, day=1)  # Replace with the real date
)

    product = Product(
        name=product_name,
        producing_company=company, 
    #ingredients=ingredients,  
        warnings="May contain peanuts. Not recommended for people with peanut allergies.",
        notes="A delicious and crunchy snack!",
        item_id=upcId, 
    )
    product.save()
    return render(request, 'main/Ingredients.html',{'response':response})
