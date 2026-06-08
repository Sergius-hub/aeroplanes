import json
from abc import ABC, abstractmethod


class BaseFileAdapter(ABC):

    @abstractmethod
    def save(self, *args):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class JSONFileAdapter(BaseFileAdapter):
    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename

    def save(self, *args):
        """Сохраняет информацию в файл"""
        if not args:
            raise ValueError("Нет объектов для сохранения")

        if not all(hasattr(arg, "to_dict") for arg in args):
            raise TypeError("Все объекты должны иметь метод to_dict()")

        data = [arg.to_dict() for arg in args]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load(self):
        """Загружает информацию из файла"""
        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def delete(self):
        pass
