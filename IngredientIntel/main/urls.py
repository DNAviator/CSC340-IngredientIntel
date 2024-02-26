from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search/", views.search_page, name="search_page"),
    path("results/<int:id>", views.results_page, name="result_page"),
    path("login/", views.login, name="login"),
    path("settings/", views.settings, name="settings"),

]
