import pytest
import requests
from .utils.config_loader import load_config
from .utils.retry import retry
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture
def base_url(config):
    return config.get("base_url", "https://httpbin.org")

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()

# Example of retryed request helper
@pytest.fixture
def request_with_retry(config):
    max_attempts = config.get("retry", {}).get("max_attempts", 3)
    backoff = config.get("retry", {}).get("backoff_seconds", 1)

    def _request(method, url, **kwargs):
        @retry(max_attempts=max_attempts, backoff_seconds=backoff, allowed_exceptions=(requests.exceptions.RequestException,))
        def do():
            return requests.request(method, url, **kwargs)
        return do()
    return _request
