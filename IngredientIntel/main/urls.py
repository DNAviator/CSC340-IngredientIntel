from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("search/", views.search_page, name="search_page"),
    path("results/<str:type>/<int:id>", views.results_page, name="result_page"),
    path("login/", views.login_page, name="login"),
    path("settings/", views.settings, name="settings"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("scan_barcode/", views.scan_barcode, name="scan_barcode"),
    path("logout/", views.logout_page, name="logout"),
    path("researcher/", views.researcher, name="researcher"),
    path("company/<str:company>/", views.company, name="company"),
    path("about/", views.about, name="about"),
    path("company_login/", views.login_page, name="company_login"),
    path("create_company/", views.create_company, name="create_company"),
    path("login/", views.login_page, name="researcher_login"),
    path('ingredient-autocomplete/', views.IngredientAutocomplete.as_view(), name='ingredient-autocomplete'),
    path("company_select/", views.select_company, name="company_select")
]
