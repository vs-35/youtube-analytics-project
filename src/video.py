import os

from googleapiclient.discovery import build


class Video:
    """ Класс для видео"""
    api_key: str = os.getenv('YT_API_KEY')  # Получен токен
    youtube = build('youtube', 'v3', developerKey=api_key)  # Специальный объект для работы с API

    def __init__(self, video_id):
        """Экземпляр инициализируется реальными данными."""
        self.video_id: str = video_id #id видео
        video_response = self._get_video_info()

        try:
            self.title: str = video_response['items'][0]['snippet']['title'] #название видео
        except IndexError:
            self.title = None

        try:
            self.url: str =f'https://www.youtube.com/videos/ {video_response["items"][0]["id"]}' #ссылка на видео
        except IndexError:
            self.url = None

        try:
            self.like_count: int = video_response['items'][0]['statistics']['likeCount'] #количество лайков
        except:
            self.like_count = None

        try:
            self.view_count: int = video_response['items'][0]['statistics']['viewCount'] #количество просмотров видео
        except:
            self.view_count = None


    def __str__(self):
        """Метод возвращает название видео"""
        return self.title

    def _get_video_info(self):
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.video_id
                                       ).execute()
        return video_response


class PLVideo(Video):

    def __init__(self, video_id, plvideo_id):
        """Класс для play-листов"""
        super().__init__(video_id)
        self.plvideo_id = plvideo_id
