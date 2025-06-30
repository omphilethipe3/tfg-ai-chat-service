import httpx
import pytest
from src.ai_agent.tools import get_person_address, check_credit_customer

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise httpx.HTTPStatusError("Error", request=None, response=None)

def test_get_person_address(monkeypatch):
    dummy = {"street": "123 Main St", "city": "Cape Town"}

    # patch httpx.get to return our dummy
    def fake_get(url):
        assert url.endswith("/persons/abc123/address")
        return DummyResponse(dummy)

    monkeypatch.setattr(httpx, "get", fake_get)

    result = get_person_address("abc123")
    assert result == dummy

def test_check_credit_customer_true(monkeypatch):
    def fake_get(url):
        return DummyResponse({"isCreditCustomer": True})

    monkeypatch.setattr(httpx, "get", fake_get)
    assert check_credit_customer("abc123") is True

def test_check_credit_customer_false(monkeypatch):
    def fake_get(url):
        return DummyResponse({"isCreditCustomer": False})

    monkeypatch.setattr(httpx, "get", fake_get)
    assert check_credit_customer("xyz789") is False