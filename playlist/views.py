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
            if 'selected_format_id' not in request.POST:
                ydl_opts = {}
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(video_url, download=False)
                        formats = info_dict.get('formats', None)
                        return render(request, 'playlist/youtube_download.html', {'formats': formats, 'video_url': video_url})

                except Exception as e:
                    return HttpResponse(f"Error: {e}")

            else:
                selected_format_id = request.POST.get('selected_format_id')
                ydl_opts = {
                    'format': selected_format_id,
                    'outtmpl': '~/Downloads/%(title)s.%(ext)s',
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(video_url, download=True)
                        video_title = info_dict.get('title', None)
                        return render(request, 'playlist/youtube_download.html', {'video_title': video_title})

                except Exception as e:
                    return HttpResponse(f"Error: {e}")

        return render(request, 'playlist/youtube_download.html')

    return render(request, 'playlist/youtube_download.html')
