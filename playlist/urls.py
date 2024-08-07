
from django.urls import path
from playlist import views

urlpatterns = [
    path('', views.index, name="homepage")
]
