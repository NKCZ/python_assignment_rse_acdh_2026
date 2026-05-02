from django.urls import path
from . import views

app_name = "apis_app"

urlpatterns = [
    path("", views.person_list, name="list"),
    path("apis_app/<str:person_id>/", views.person_detail, name="detail"),
]