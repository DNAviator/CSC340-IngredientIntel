from django.apps import AppConfig
from django.urls import path
#from django.urls import include
from django.conf.urls.static import static
from django.contrib.staticfiles import finders
from django.conf import settings
import os

import cv2
# from pyzbar.pyzbar import decode

#barcode = cv2.imread(static("images/peanuts.png"))
def barcode_decoder() :

    #url = static("images/peanuts.png")

    #path("static/", , name="researcher")
    #image_path = finders.find('images/peanut.png')
    url = "static/images/peanut.png"
    #url = os.path.dirname(image_path)
    #url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("hi", url)
    #barcode = cv2.imread(url)
    #for code in decode(barcode) :
    #    print(code.type)
    #    print(code.data)