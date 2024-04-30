# Ingredient Intel

## Team Members
> Justin Evans, Joseph Cramer, Pradhyumna Kothapalli

## Description
Forget deciphering long and confusing labels! Ingredient Intel (INI), a revolutionary app for Android and web, empowers you to make informed food choices. Scan any product's barcode to access clear ingredient breakdowns, potential allergens, and health effects. Set dietary preferences and get alerts for unwanted ingredients. Companies benefit too, with easy ingredient management, recall communication, and transparency tools. Research institutions also play a role with access to contribute scientific notes, keeping consumers informed about the latest health findings. With the database connected to the FDA's API, Ingredient Intel prioritizes safety by automatically flagging recalled products. Eat healthier, make informed choices, and unlock a transparent future with Ingredient Intel.

![project diagram](https://github.com/DNAviator/CSC340-IngredientIntel/blob/main/UseCaseModel.PNG)

## How to use
1. Clone repository to computer
2. Download a suitable IDE (I use vscode)
3. Open the folder as a workspace or project and create a venv (or other environment)
4. Using pip within the venv install the packages:  
    a. python -m pip install Django   
    b. python -m pip install psycopg2   
    c. python -m pip install Pillow  
    d. python -m pip install cv2  
    e. python -m pip install pyzbar   
    f. python -m pip install requests   
    g. python -m pip install django-autocomplete-light  
    h. python -m pip install django-cleanup  
5. Use existing database by contacting us (JCramerOfficial@gmail.com) or follow database setup instructions
    a. Download postgreSQL 16 from https://www.postgresql.org/download/  
    b. Using installer (or by following a manual tutorial found online) setup the database on port 5432 (default)
        and have it run on localhost. Set the username and table name to postgres and remember the password you set.  
    c. Create a file secrets.json in the base directory (CSC340-IngredientIntel) with the text:  
        {  
    "DEV_KEY": (insert dev key),  
    "DB_PSWD": (insert password for database),  
    "DB_HOST": (enter localhost)  
        }  
    d. At this point you should be able to run the server by navigating to the IngredientIntel directory and
        using the command "python manage.py runserver" do so to test for errors  
    e. After stopping the server (with break or ctr+c) run these commands:  
        - python manage.py migrate  
        - python manage.py makemigrations main  
        - python manage.py migrate  
    f. At this point your database should be setup and the server ready to use, you may want to create an admin account
        however and to do so stop the server and run the command: "python manage.py createsuperuser" which will prompt you in setting up an admin  
6. You are ready to go! (note you may need to replace the api key found in views.py with a new one from the FDC api to have api functionality)  
