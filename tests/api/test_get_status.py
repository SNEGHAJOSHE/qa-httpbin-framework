import pytest

def test_status_200(base_url, request_with_retry):
    url = f"{base_url}/status/200"
    resp = request_with_retry("GET", url, timeout=10)
    assert resp.status_code == 200

def test_status_418(base_url, request_with_retry):
    url = f"{base_url}/status/418"
    resp = request_with_retry("GET", url, timeout=10)
    assert resp.status_code == 418
