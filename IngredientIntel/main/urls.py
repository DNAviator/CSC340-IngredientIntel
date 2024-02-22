from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:query>", views.search_page, name="search_page"),
    path("results/<str:type>/<str:object>", views.result_page, name="result_page"),
]
