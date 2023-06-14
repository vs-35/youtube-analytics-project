import os
from googleapiclient.discovery import build

class PlayList:
    """ Класс для play-листов канала"""
    def __init__(self, pl_id):
        """Экземпляр инициализируется реальными данными."""
        self.pl_id: str = pl_id #id play-листа
        playlist_videos = self._get_pl_info()
        video_response = self._get_video_info()
        self.title: str = playlist_videos['items'][0]['snippet']['title'] #название play-листа
        self.url: str =f'https://www.youtube.com/playlist/ {playlist_videos["items"][0]["id"]}' #ссылка на play-лист
        self.like_count_video: int = video_response['items'][0]['statistics']['likeCount'] #количество лайков


    def _get_pl_info(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.pl_id, part='contentDetails', maxResults=50,).execute()
        return playlist_videos


    def _get_video_info(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.pl_id, part='contentDetails',
                                                                  maxResults=50, ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """ Метод для определения общего времени play-листа"""
        total_duration = timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time = str(duration).split(":")
            duration = timedelta(hours = int(time[0]), minutes = int(time[1]), seconds = int(time[2]))
            total_duration += duration
            return total_duration


    def __str__(self):
        """Метод возвращает общую продолжительность play-листа"""
        return total_duration

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')  # Получен токен
        youtube = build('youtube', 'v3', developerKey=api_key)  # Специальный объект для работы с API
        return youtube

    def show_best_video(self):
            self.like_count_video = video_response['items'][0]['statistics']['likeCount'].sort(reverse=True)
            max_like_video = self.like_count_video[0]
            return max_like_video