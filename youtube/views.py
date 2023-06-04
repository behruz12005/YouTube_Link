from django.shortcuts import render
from googleapiclient.discovery import build
from .models import YouTobeModel,Comment
import googleapiclient.discovery
import os
from django.shortcuts import render, get_object_or_404
def Home(request):
    data = YouTobeModel.objects.all()

    if request.method == 'POST':
        video_link = request.POST['videoLink']
        video_id = video_link.split('=')[1]
        video_id = video_id.split('&')[0]

        api_key = 'AIzaSyCq7Q0ELgdp9VjTcPyytE9dyWJg8rXEo5I'
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        ).execute()

        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

        api_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = api_request.execute()

        comments = response["items"]

        for comment in comments:
            # Komment matnini olishish
            text1 = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

            # Komment sanasini olishish
            date = comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

            # Avtorni olishish
            author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]

            # Avtor haqida qo'shimcha ma'lumotlarni olishish
            author_info = comment["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]

            # Avtor profil URL sini olishish
            author_profile_url = "https://www.youtube.com/channel/" + author_info['value']

            # Commentlar bilan Comment modelini to'ldirish
            comment_model = Comment(
                text_id=video_id,
                text=text1,
                date=date,
                author=author,
                author_info=author_info,
                author_profile_url=author_profile_url
            )
            comment_model.save()

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

    return render(request, 'home.html', {'data': data})



def comment(request, pk):
    comment_obj = get_object_or_404(YouTobeModel, pk=pk)
    video_id = comment_obj.video_id
    comments = Comment.objects.filter(text_id=video_id)
    
    return render(request, 'comment.html', {'video_id': video_id, 'comments': comments})







# def Commnet(request):
#     data = Comment.objects.all()

#     if request.method == 'POST':
#         try:
#             os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#             api_service_name = "youtube"
#             api_version = "v3"
#             DEVELOPER_KEY = "AIzaSyCq7Q0ELgdp9VjTcPyytE9dyWJg8rXEo5I"

#             youtube = googleapiclient.discovery.build(
#                 api_service_name, api_version, developerKey=DEVELOPER_KEY)

#             video_id = "01sAkU_NvOY"

#             request = youtube.commentThreads().list(
#                 part="snippet",
#                 videoId=video_id,
#                 maxResults = 100
#             )
#             response = request.execute()

#             comments = response["items"]
#             # comment_count = len(comments)

#             for comment in comments:
#                 # Komment matnini olishish
#                 text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

#                 # Komment sanasini olishish
#                 date = comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

#                 # Avtorni olishish
#                 author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]

#                 # Avtor haqida qo'shimcha ma'lumotlarni olishish
#                 author_info = comment["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]

#                 # Avtor profil URL sini olishish
#                 author_profile_url = "https://www.youtube.com/channel/" + author_info['value']

#             # Commentlar ro'yxatini olish

#             # Commentlar bilan Comment modelini to'ldirish
#                 comment_model = Comment(
#                     text=text,
#                     date=date,
#                     author=author,
#                     author_info=author_info,
#                     author_profile_url=author_profile_url
#                 )
#                 comment_model.save()

#             return render(request, 'home.html', {
#                 'video_title': video_title,
#                 'channel_title': channel_title,
#                 'description': description,
#                 'view_count': view_count,
#                 'data': data
#             })
#         except:
#             text = 'Sizda yaroqsiz link yoki takrorlangan link berdingiz. Malumot saqlanmadi !.'
#             return render(request, 'home.html', {'data': data, 'text': text})

#     return render(request, 'home.html', {'data': data})
