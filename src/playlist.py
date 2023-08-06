import os
import datetime
import isodate
from googleapiclient.discovery import build
from src.video import Video

class PlayList:
    """Класс для получения информации о плейлисте"""
    API_KEY: str = os.getenv('YOUTUBE_API_KEY')
    YOUTYBE = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id: str) -> None:
        """Конструктор класса"""

        # Получаем информацию в виде словаря (необходимо для получения названия плейлиста)
        self.playlist_info = PlayList.YOUTYBE.playlists().list(id=playlist_id,
                                                               part='snippet,contentDetails',
                                                               maxResults=50).execute()

        # Получаем информацию в виде словаря (необходимо для получения информации о видеороликах)
        self.playlist = PlayList.YOUTYBE.playlistItems().list(playlistId=playlist_id,
                                                              part='snippet,contentDetails,id,status',
                                                              maxResults=50).execute()

        # Получаем id всех видеороликов
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]

        # Получаем длительность всех видеороликов
        video_response = PlayList.YOUTYBE.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)).execute()

        # Определяем общую длительность видеороликов
        delta = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            delta += duration

        self.title = self.playlist_info["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        self.__total_duration = delta

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        # Получаем id всех видеороликов
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]

        # Ищем самое популярное видео
        max_count_of_likes = 0
        for row in video_ids:
            video = Video(row)
            if int(video.number_of_likes) > max_count_of_likes:
                best_video = video
        
        return best_video.url
