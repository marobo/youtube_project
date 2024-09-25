import yt_dlp
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    my_dict = {"insert_me": "I am from views.py"}
    return render(request, 'index.html', context=my_dict)


def youtube_playlist(request):
    return render(request, 'playlist/youtube_playlist.html')


def youtube_downloader(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if video_url:
            ydl_opts = {
                'format': 'best',  # You can adjust this for video or audio formats
                'outtmpl': '~/Downloads/%(title)s.%(ext)s',  # Directory to save files
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_title = info_dict.get('title', None)
                    file_name = f"{video_title}.mp4"  # Adjust this to your needs

                    # After download, you can return the file path or further process it
                    return HttpResponse(f"Video '{video_title}' downloaded successfully as {file_name}")
            except Exception as e:
                return HttpResponse(f"Error: {e}")

    return render(request, 'playlist/youtube_downloader.html')
