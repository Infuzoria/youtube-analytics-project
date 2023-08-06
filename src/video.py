import os
from googleapiclient.discovery import build


class Video():
    """Класс для получения информации о видео"""
    API_KEY: str = os.getenv('YOUTUBE_API_KEY')
    YOUTYBE = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id: str):
        """Конструктор класса"""

        # Получаем данные в виде словаря
        video = Video.YOUTYBE.videos().list(part='snippet,statistics', id=video_id).execute()

        # Вычленяем нужную информацию
        self.video_id = video_id
        self.title = video["items"][0]["snippet"]["title"]
        self.url = "https://youtu.be/" + video_id
        self.number_of_views = video["items"][0]["statistics"]["viewCount"]
        self.number_of_likes = video["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """Вывод данных об объекте в пользовательском режиме"""
        return self.title


class PLVideo(Video):
    """Класс для получения информации о видео и плейлисте"""

    def __init__(self, video_id: str, playlist_id: str):
        """Конструктор класса"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
