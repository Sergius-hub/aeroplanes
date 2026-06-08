import pytest
from unittest.mock import Mock, patch
from src.api_adapter import HTTPAdapter, Response


class TestHTTPAdapter:
    """Тесты для HTTPAdapter"""

    def test_init_valid_request(self):
        """Создание адаптера с валидным запросом"""
        request = {"url": "https://api.example.com/data"}
        adapter = HTTPAdapter(request)

        assert adapter._request == request
        assert adapter._response is None

    def test_init_request_none(self):
        """Создание адаптера с None -> ошибка"""
        with pytest.raises(ValueError, match="request не может быть None"):
            HTTPAdapter(None)  # type: ignore

