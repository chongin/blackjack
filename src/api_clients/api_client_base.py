import requests
from logger import Logger

class ApiClientBase:
    def __init__(self, endpoint, timeout=10) -> None:
        self.endpoint = endpoint
        self.timeout = timeout

    def make_request(self, url_suffix, method="GET", data=None) -> dict:
        full_url = f"{self.endpoint}/{url_suffix}"
        try:
            if method == "GET":
                response = requests.get(full_url, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(full_url, json=data, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
            return response.json()
        except requests.exceptions.Timeout as e:
            Logger.error(f"Request timed out: {e}", full_url)
        except requests.exceptions.RequestException as e:
            Logger.error(f"Request exception: {e}", full_url)
        except Exception as e:
            Logger.error(f"An unexpected error occurred: {e}", full_url)