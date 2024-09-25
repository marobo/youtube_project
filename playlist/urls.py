
from django.urls import path
from playlist import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('playlist/', views.youtube_playlist, name='youtube_playlist'),
    path('download/', views.youtube_downloader, name='youtube_downloader'),
]
