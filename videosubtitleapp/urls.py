from django.contrib import admin
from django.urls import path, include
from . import views

from .views import SearchView


urlpatterns = [
    path("", views.upload_video),
    path('search/', SearchView.as_view(), name='search'),
]
