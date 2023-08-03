import os
import datetime
import isodate
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

        # Получаем id всех видеороликов
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]

        # Получаем длительность всех видеороликов
        video_response = PlayList.YOUTYBE.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)).execute()

        # Определяем общую длительность видеороликов
        delta = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            delta += duration

        self.title = playlist["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        self.__total_duration = delta

    @property
    def total_duration(self):
        return self.__total_duration


pl = PlayList("PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw")
print(pl.total_duration)
