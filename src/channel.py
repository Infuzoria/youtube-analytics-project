import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    API_KEY: str = os.getenv('YOUTUBE_API_KEY')
    DATA_FILE = "/home/shurochka/PycharmProjects/youtube-analytics-project2/data.json"
    YOUTYBE = build('youtube', 'v3', developerKey=API_KEY)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""

        # Получаем данные в виде словаря
        channel = Channel.YOUTYBE.channels().list(id=channel_id, part='snippet,statistics').execute()

        # Вычленяем необходимую информацию
        self.channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.link = channel["items"][0]["snippet"]["customUrl"]
        self.number_of_subscribers = channel["items"][0]["statistics"]["subscriberCount"]
        self.number_of_video = channel["items"][0]["statistics"]["videoCount"]
        self.number_of_views = channel["items"][0]["statistics"]["viewCount"]


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.YOUTYBE.channels().list(id = self.channel_id,
        part = 'snippet,statistics').execute()
        print(channel)


    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.YOUTYBE


    def to_json(self) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """

        # Записываем необходимые данные в словарь
        dictionary = {"channel_id": self.channel_id, "title": self.title,
                      "description": self.description, "link": self.link,
                      "number_of_subscribers": self.number_of_subscribers,
                      "number_of_video": self.number_of_video,
                      "number_of_views": self.number_of_views}

        # Записываем данные в json файл
        if os.stat(Channel.DATA_FILE).st_size == 0:
            with open(Channel.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([dictionary], f, ensure_ascii=False)
        else:
            with open(Channel.DATA_FILE, "r", encoding="utf-8") as f:
                data_list = json.load(f)
            data_list.append(dictionary)
            with open(Channel.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False)
