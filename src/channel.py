import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""
        self.channel_id = channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey = Channel.api_key)
        channel = youtube.channels().list(id = self.channel_id,
        part = 'snippet,statistics').execute()
        print(channel)
