import os
import uuid
import boto3
import subprocess

from celery import shared_task
from django.conf import settings

from botocore.exceptions import NoCredentialsError

from .models import Video
from decouple import config
import re
from datetime import datetime 

dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

table = dynamodb.Table(config('Dynamodb_Table_Name'))

def store_subtitle_keywords(video_id, text, start_time, end_time):
    words = text.split()
    
    for word in words:
        table.put_item(
            Item={
                'word': word.lower(),
                'video_id': str(video_id),
                'start_time': start_time,
                'end_time': end_time,
            }
        )

def store_subtitle_phrase(video_id, text, start_time, end_time):
    table.put_item(
        Item={
            'word': text,
            'video_id': str(video_id),
            'start_time': start_time,
            'end_time': end_time,
        }
    )

def process_subtitles(video_id, subtitle_filepath):
    print("Keywords are being incorporated into DynamoDB.")
    video = Video.objects.get(pk=video_id)

    timestamp_regex = r"\d{2}:\d{2}:\d{2},\d{3}"

    with open(subtitle_filepath, 'r') as file:
        subtitle_text = file.read()

    subtitles = re.split(r"\n\n", subtitle_text)

    for subtitle in subtitles:
        # Extract timestamp
        matches = re.findall(timestamp_regex, subtitle)
        
        if len(matches) != 2:
            continue

        start_time = str(datetime.strptime(matches[0], "%H:%M:%S,%f").time())
        end_time = str(datetime.strptime(matches[1], "%H:%M:%S,%f").time())

        subtitle_lines = subtitle.split("\n")
        
        if len(subtitle_lines) < 3:
            continue

        text_lines = subtitle_lines[2:]
        
        text = " ".join(" ".join(text_lines).split()).lower()

        store_subtitle_phrase(video_id, text, start_time, end_time)

        words = text.split()
        for word in words:
            store_subtitle_keywords(video_id, word, start_time, end_time)

    print('Done')

        
@shared_task
def extract_subtitles(video_id):
    print('The CCExtractor binary is used for extracting subtitles from videos.')
    video = Video.objects.get(pk=video_id)
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    video_filename = os.path.splitext(video.file.name)[0].replace('videos/', '')

    unique_filename = f"{video_filename}-{uuid.uuid4()}"
    
    local_video_filepath = os.path.join(os.path.expanduser('~'), f"{unique_filename}.mp4")
    subtitle_filepath = os.path.join(os.path.expanduser('~'), f"{unique_filename}.srt")

    s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, str(video.file), local_video_filepath)
    
    cmd = f'ccextractor {local_video_filepath} -o {subtitle_filepath}'
    subprocess.run(cmd, check=True, shell=True)

    with open(subtitle_filepath, 'rb') as data:
        s3.upload_fileobj(data, settings.AWS_STORAGE_BUCKET_NAME, f'subtitles/{unique_filename}.srt')

    video.subtitles = f'subtitles/{unique_filename}.srt'  
    video.save()

    process_subtitles(video.id, subtitle_filepath)

    os.remove(local_video_filepath)
    os.remove(subtitle_filepath)
    
    print('Done')
