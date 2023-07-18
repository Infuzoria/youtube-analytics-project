import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""

        # Получаем данные в виде словаря
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.link = channel["items"][0]["snippet"]["customUrl"]
        self.number_of_subscribers = channel["items"][0]["statistics"]["subscriberCount"]
        self.number_of_video = channel["items"][0]["statistics"]["videoCount"]
        self.number_of_views = channel["items"][0]["statistics"]["viewCount"]


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey = Channel.api_key)
        channel = youtube.channels().list(id = self.channel_id,
        part = 'snippet,statistics').execute()
        print(channel)
