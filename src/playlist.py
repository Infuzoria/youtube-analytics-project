import os
from googleapiclient.discovery import build


class PlayList:
    """Класс для получения информации о плейлисте"""
    API_KEY: str = os.getenv('YOUTUBE_API_KEY')
    YOUTYBE = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id: str) -> None:
        """Конструктор класса"""

        # Получаем информацию в виде словаря
        playlist = PlayList.YOUTYBE.playlistItems().list(playlistId=playlist_id,
                                                         part='snippet,contentDetails,id,status',
                                                         maxResults=50).execute()

        self.title = playlist["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
