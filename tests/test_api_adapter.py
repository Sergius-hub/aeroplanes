from unittest.mock import Mock, patch

import pytest

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

    def test_get_response(self):
        """Проверка метода get_response"""
        pass

    def test_get_response_first_call(self):
        """Тест: первый вызов get_response -> вызывает _fetch"""
        request = {"url": "https://api.example.com/data"}
        adapter = HTTPAdapter(request)

        mock_response = Mock(spec=Response)
        mock_response.status_code = 200

        with patch.object(adapter, "_fetch", return_value=mock_response) as mock_fetch:
            response = adapter.get_response()

            assert response == mock_response
            assert adapter._response == mock_response
            mock_fetch.assert_called_once()

    def test_fetch_direct_call(self):
        """Прямой вызов _fetch для проверки логики"""
        request = {"url": "https://httpbin.org/get", "params": {"test": 1}}
        adapter = HTTPAdapter(request)

        # Временно подменяем внешнюю зависимость
        mock_response = Mock(spec=Response)
        mock_response.raise_for_status = Mock()

        with patch("src.api_adapter.get", return_value=mock_response) as mock_get:
            response = adapter._fetch()

            # Проверяем, что get был вызван с правильными параметрами
            mock_get.assert_called_once_with(**request)

            # Проверяем, что raise_for_status был вызван
            mock_response.raise_for_status.assert_called_once()

            # Проверяем, что _fetch вернул ответ
            assert response == mock_response
