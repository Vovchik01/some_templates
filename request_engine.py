import requests
import time
from typing import Dict, Any, Optional

class RequestHandler:
    """Base class for request handlers."""
    def handle_request(self, request: Dict[str, Any], timeout: Optional[float] = None) -> Any:
        """Handle the request."""
        pass

class HTTPRequestHandler(RequestHandler):
    """Handles HTTP requests."""
    def __init__(self, method: str):
        """
        Initialize the HTTPRequestHandler.

        Args:
            method (str): The HTTP method (e.g., "get", "post").
        """
        self.method = method

    def handle_request(self, request: Dict[str, Any], timeout: Optional[float] = None) -> Any:
        """
        Handle the HTTP request.

        Args:
            request (Dict[str, Any]): The request parameters.
            timeout (Optional[float]): The request timeout in seconds.

        Returns:
            Any: The response content.
        """
        url = request.get("url")
        session = request.get("session")
        proxies = request.get("proxies")
        response = self.send_request(url, request.get("data"), session, proxies, timeout)
        return self.handle_response(response)

    def send_request(self, url: str, data: Optional[Dict[str, Any]], session: Optional[requests.Session], proxies: Optional[Dict[str, str]], timeout: Optional[float] = None) -> requests.Response:
        """
        Send the HTTP request.

        Args:
            url (str): The URL for the request.
            data (Optional[Dict[str, Any]]): The request data.
            session (Optional[requests.Session]): The requests session object.
            proxies (Optional[Dict[str, str]]): Proxy configuration.
            timeout (Optional[float]): The request timeout in seconds.

        Returns:
            requests.Response: The response object.
        """
        method_func = getattr(session or requests, self.method)
        return method_func(url, data=data, proxies=proxies, timeout=timeout)

    def handle_response(self, response: requests.Response) -> Any:
        """
        Handle the HTTP response.

        Args:
            response (requests.Response): The response object.

        Returns:
            Any: The response content.
        """
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text

class HTTPGetHandler(HTTPRequestHandler):
    """Handles HTTP GET requests."""
    def __init__(self):
        """Initialize the HTTPGetHandler."""
        super().__init__("get")

class HTTPPostHandler(HTTPRequestHandler):
    """Handles HTTP POST requests."""
    def __init__(self):
        """Initialize the HTTPPostHandler."""
        super().__init__("post")

class RequestEngine:
    """Manages and handles various types of requests."""
    def __init__(self):
        """Initialize the RequestEngine."""
        self.handlers: Dict[str, RequestHandler] = {
            "HTTP_GET": HTTPGetHandler(),
            "HTTP_POST": HTTPPostHandler()
        }

    def add_handler(self, request_type: str, handler: RequestHandler) -> None:
        """
        Add a request handler.

        Args:
            request_type (str): The type of request.
            handler (RequestHandler): The request handler.
        """
        self.handlers[request_type] = handler

    def handle_request(self, request: Dict[str, Any], max_retries: int = 3, retry_delay: int = 1, timeout: Optional[float] = None) -> Any:
        """
        Handle a request.

        Args:
            request (Dict[str, Any]): The request parameters.
            max_retries (int, optional): The maximum number of retries. Defaults to 3.
            retry_delay (int, optional): The delay between retries in seconds. Defaults to 1.
            timeout (Optional[float]): The request timeout in seconds.

        Returns:
            Any: The response content.
        """
        request_type = request.get("type")
        handler = self.handlers.get(request_type)
        if handler:
            return self._retry_request(handler, request, max_retries, retry_delay, timeout)
        else:
            print(f"Unsupported request type: {request_type}")
            return None

    def _retry_request(self, handler: RequestHandler, request: Dict[str, Any], max_retries: int, retry_delay: int, timeout: Optional[float] = None) -> Any:
        """
        Retry handling a request.

        Args:
            handler (RequestHandler): The request handler.
            request (Dict[str, Any]): The request parameters.
            max_retries (int): The maximum number of retries.
            retry_delay (int): The delay between retries in seconds.
            timeout (Optional[float]): The request timeout in seconds.

        Returns:
            Any: The response content.
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = handler.handle_request(request, timeout)
                return response  # Successful request, no need for retries
            except Exception as e:
                print(f"Request failed: {e}")
                retry_count += 1
                print(f"Retrying ({retry_count}/{max_retries})...")
                time.sleep(retry_delay)
        print("Max retries reached, request failed.")
        return None

# Example client code
if __name__ == "__main__":
    engine = RequestEngine()

    get_request = {"type": "HTTP_GET", "url": "https://www.example.com"}
    post_request = {"type": "HTTP_POST", "url": "https://www.example.com", "data": {"key": "value"}}

    get_response = engine.handle_request(get_request, timeout=10)
    post_response = engine.handle_request(post_request, timeout=10)

    if get_response:
        print("GET Response:")
        print(get_response)

    if post_response:
        print("POST Response:")
        print(post_response)
