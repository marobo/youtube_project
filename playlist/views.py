import yt_dlp, os, mimetypes
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


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
                download_path = os.path.join(settings.MEDIA_ROOT, 'downloaded_files')
                os.makedirs(download_path, exist_ok=True)
                ydl_opts = {
                    'format': selected_format_id,
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(video_url, download=True)
                        video_title = info_dict.get('title', None)
                        file_path = os.path.join(download_path, f"{video_title}.{info_dict['ext']}")

                        # Serve the file
                        with open(file_path, 'rb') as f:
                            response = HttpResponse(f.read())
                            content_type = mimetypes.guess_type(file_path)[0]
                            response['Content-Type'] = content_type
                            response['Content-Disposition'] = f'attachment; filename="{video_title}.{info_dict["ext"]}"'

                            try:
                                os.remove(file_path)
                                return render(request, 'playlist/youtube_download.html', {'video_title': video_title})

                            except Exception as e:
                                print(f"Error deleting file: {e}")

                            return response

                except Exception as e:
                    return HttpResponse(f"Error: {e}")

        return render(request, 'playlist/youtube_download.html')

    return render(request, 'playlist/youtube_download.html')
