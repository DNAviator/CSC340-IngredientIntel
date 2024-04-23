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
    path("researcher_signup/", views.researcher_signup, name="researcher_signup"),
    path("researcher_login/", views.researcher_login, name="researcher_login"),
    path("company/<str:company>/", views.company, name="company"),
    path("about/", views.about, name="about"),
    path("create_company/", views.create_company, name="create_company"),
    path('ingredient-autocomplete/', views.IngredientAutocomplete.as_view(), name='ingredient-autocomplete'),
    path("company_select/", views.select_company, name="company_select"),
    path("update/<str:model_type>/<int:item_id>/", views.update_item, name="update"),
    path("update_backend/<str:model_type>/<int:item_id>/", views.update_backend, name="update_backend"),
    path("delete/<str:model_type>/<int:item_id>/", views.delete_product, name="delete"),
    path("ingred",views.fetch_api_data, name = "Ingredients")
]
