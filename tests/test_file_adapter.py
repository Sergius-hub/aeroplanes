import json

import pytest

from src.file_adapter import JSONFileAdapter


def test_initialization_jsonfileadapter():
    """Проверяем, что объект правильно создается"""
    adapter = JSONFileAdapter()
    assert adapter.filename == "data/aeroplanes.json"


def test_save_with_objects_without_to_dict_raises_error():
    """Сохранение объектов без метода to_dict -> TypeError"""
    adapter = JSONFileAdapter("test.json")

    class WithoutToDict:
        pass

    with pytest.raises(TypeError, match="Все объекты должны иметь метод to_dict()"):
        adapter.save(WithoutToDict(), WithoutToDict())


# def test_save_valid_objects(tmp_path):
#     """Сохранение валидных объектов"""
#     file_path = tmp_path / "test.json"
#     adapter = JSONFileAdapter(str(file_path))
#
#     # Создаем объекты с to_dict
#     class TestObject:
#         def __init__(self, name, value):
#             self.name = name
#             self.value = value
#
#         def to_dict(self):
#             return {"name": self.name, "value": self.value}
#
#     obj1 = TestObject("first", 100)
#     obj2 = TestObject("second", 200)
#
#     adapter.save(obj1, obj2)
#
#     # Проверяем содержимое файла
#     assert file_path.exists()
#     with open(file_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#
#     assert data == [{"name": "first", "value": 100}, {"name": "second", "value": 200}]
