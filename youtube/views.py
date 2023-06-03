from django.shortcuts import render
from googleapiclient.discovery import build
from .models import YouTobeModel

def Home(request):
    data = YouTobeModel.objects.all()

    if request.method == 'POST':
        try:
            video_link = request.POST['videoLink']
            video_id = video_link.split('=')[1]
            video_id = video_id.split('&')[0]

            api_key = 'AIzaSyCq7Q0ELgdp9VjTcPyytE9dyWJg8rXEo5I'
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()

            video_info = video_response.get('items', [])
            if video_info:
                video_info = video_info[0]
            else:
                video_info = {}

            video_title = video_info.get('snippet', {}).get('title', '')
            channel_title = video_info.get('snippet', {}).get('channelTitle', '')
            description = video_info.get('snippet', {}).get('description', '')
            view_count = video_info.get('statistics', {}).get('viewCount', '')

            content_model = YouTobeModel(
                video_id=video_id,
                channelTitle=channel_title,
                title=video_title,
                viewCount=int(view_count),
                description=description
            )
            content_model.save()

            return render(request, 'home.html', {
                'video_title': video_title,
                'channel_title': channel_title,
                'description': description,
                'view_count': view_count,
                'data': data
            })
        except:
            text = 'Sizda yaroqsiz link yoki takrorlangan link berdingiz. Malumot saqlanmadi !.'
            return render(request, 'home.html', {'data': data, 'text': text})

    return render(request, 'home.html', {'data': data})
