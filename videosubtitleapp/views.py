from django.shortcuts import render
from .forms import VideoForm
from .tasks import extract_subtitles

from django.http import JsonResponse
from django.views import View

import boto3
from django.conf import settings
from boto3.dynamodb.conditions import Key, Attr
from decouple import config
from django.views.generic import TemplateView

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            print("The video is getting stored in S3.")
            video = form.save()
            print("It has been included in the background task.")
            extract_subtitles.delay(video.id)
    else:
        form = VideoForm()
    return render(request, 'videosubtitleapp/upload_video.html', {'form': form})

class SearchView(TemplateView):
    template_name = 'videosubtitleapp/upload_video.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        
        if not keyword:
            context['error'] = "Missing 'keyword' parameter."
            return context

        dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        table = dynamodb.Table(config('Dynamodb_Table_Name'))

        response = table.scan(
            FilterExpression=Attr('word').contains(keyword.lower())
        )
        
        items = response['Items']

        if not items:
            context['error'] = "No video found with the given keyword."
            return context
        
        results = []
        for item in items:
            results.append({
                "video_id": item["video_id"],
                "start_time": item["start_time"],
                "end_time": item["end_time"],
            })

        context['results'] = results
        return context