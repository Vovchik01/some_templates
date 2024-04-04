import pytest
from request_engine import RequestEngine

@pytest.fixture
def request_engine():
    return RequestEngine()

def test_get_request(request_engine):
    get_request = {"type": "HTTP_GET", "url": "https://www.example.com"}
    response = request_engine.handle_request(get_request)
    assert response is not None
    assert "<html" in response  # Checking if HTML content is present

def test_post_request(request_engine):
    post_request = {"type": "HTTP_POST", "url": "https://www.example.com", "data": {"key": "value"}}
    response = request_engine.handle_request(post_request)
    assert response is not None
    assert "Success" in response  # Assuming the server returns "Success" upon successful POST

def test_invalid_request_type(request_engine):
    invalid_request = {"type": "INVALID", "url": "https://www.example.com"}
    response = request_engine.handle_request(invalid_request)
    assert response is None

def test_timeout(request_engine):
    get_request = {"type": "HTTP_GET", "url": "https://www.example.com"}
    response = request_engine.handle_request(get_request, timeout=0.1)  # Setting a very short timeout
    assert response is None  # Expecting None due to timeout

if __name__ == "__main__":
    pytest.main()
