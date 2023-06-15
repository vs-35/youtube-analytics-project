import os

from datetime import timedelta
from googleapiclient.discovery import build

import isodate
import json

api_key: str = os.getenv('YT_API_KEY')# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
youtube = build('youtube', 'v3', developerKey=api_key) # специальный объект для работы с API
class PlayList:
    """Класс `PlayList`, который инициализируется _id_ плейлиста"""

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={self.playlist_id}' #ссылка на play-лист'

    @property
    def total_duration(self):
        """ Метод для определения общего времени play-листа"""
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']] #все id видеороликов из плейлиста

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_duration = timedelta(hours=0, minutes=0, seconds=0)

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        sorted_like_count = sorted(video_response['items'], key=lambda x: int(x['statistics']['likeCount']),
                                       reverse=True)
        max_like_count_videoid = sorted_like_count[0]['id']
        return f"https://youtu.be/{max_like_count_videoid}"