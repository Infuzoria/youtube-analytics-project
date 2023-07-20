import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    API_KEY: str = os.getenv('YOUTUBE_API_KEY')
    YOUTYBE = build('youtube', 'v3', developerKey = API_KEY)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""

        # Получаем данные в виде словаря
        channel = Channel.YOUTYBE.channels().list(id = channel_id,
        part = 'snippet,statistics').execute()

        # Вычленяем необходимую информацию
        self.__channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = "https: / / www.youtube.com / channel / " + channel_id
        self.number_of_subscribers = channel["items"][0]
        ["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.number_of_views = channel["items"][0]["statistics"]["viewCount"]


    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону"""
        return f"{self.title} ({self.url})"


    def __add__(self, other):
        """Метод для операции сложения"""
        return self.number_of_subscribers + other.number_of_subscribers


    def __sub__(self, other):
        """Метод для операции вычитания"""
        return self.number_of_subscribers - other.number_of_subscribers


    @property


    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.YOUTYBE.channels().list(id = self.channel_id,
        part = 'snippet,statistics').execute()
        print(channel)


    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.YOUTYBE


    def to_json(self, filename: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """

        # Записываем необходимые данные в словарь
        dictionary = {"channel_id": self.channel_id, "title": self.title,
        "description": self.description, "link": self.url,
        "number_of_subscribers": self.number_of_subscribers,
        "number_of_video": self.video_count,
        "number_of_views": self.number_of_views}

        # Записываем данные в json файл
        try:
            os.stat(filename).st_size == 0
        except FileNotFoundError as e:
            with open(filename, "x", encoding = "utf - 8") as f:
                json.dump([dictionary], f, ensure_ascii = False)
        else:
            with open(filename, "r", encoding = "utf - 8") as f:
                data_list = json.load(f)
            data_list.append(dictionary)
            with open(filename, "a", encoding = "utf - 8") as f:
                json.dump(data_list, f, ensure_ascii = False)


ch1 = Channel("UC-OVMPlMA3-YCIeg4z5z23A")
print(ch1)
