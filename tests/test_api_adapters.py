import pytest
from unittest.mock import Mock, patch
from src.api_adapter import HTTPAdapter
from src.api_adapters import AdapterNominatimAPI, AdapterOpenskyAPI


def test_nominatim_init():
    adapter = AdapterNominatimAPI()

    assert adapter._request["url"] == "https://nominatim.openstreetmap.org/search"
    assert adapter._request["headers"] == {"User-Agent": "test-app/1.0"}
    assert adapter._request["params"] == {
        "country": "Canada",
        "format": "json",
        "limit": 1,
    }
