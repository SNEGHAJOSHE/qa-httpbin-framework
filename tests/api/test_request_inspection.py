import json
from ..utils.data_factory import random_user

def test_post_inspect_json(base_url, request_with_retry):
    data = random_user()
    url = f"{base_url}/post"
    resp = request_with_retry("POST", url, json=data, timeout=10)
    assert resp.status_code == 200
    body = resp.json()
    # httpbin echoes back json under 'json' key
    assert body['json'] == data

def test_response_formats(base_url, request_with_retry):
    # json, xml, plain text endpoints in httpbin
    r_json = request_with_retry("GET", f"{base_url}/json", timeout=10)
    assert r_json.status_code == 200
    assert 'slideshow' in r_json.json()

    r_xml = request_with_retry("GET", f"{base_url}/xml", timeout=10)
    assert r_xml.status_code == 200
    assert b"<?xml" in r_xml.content

    r_html = request_with_retry("GET", f"{base_url}/html", timeout=10)
    assert r_html.status_code == 200
    assert "<html" in r_html.text.lower()
