from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from playlist import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('playlist/', views.youtube_playlist, name='youtube_playlist'),
    path('download/', views.youtube_downloader, name='youtube_downloader'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
