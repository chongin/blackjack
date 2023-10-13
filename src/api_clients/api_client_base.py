import requests
from logger import Logger
from exceptions.system_exception import TimeoutException, RequestException, RequestUnhandleException
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
            # response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
            return response.json()
        except requests.exceptions.Timeout as e:
            Logger.error(f"Request timed out: {str(e)}", full_url)
            raise TimeoutException(f"Request timed out: {str(e)}")
        except requests.exceptions.RequestException as e:
            Logger.error(f"Request exception: {str(e)}", full_url)
            raise RequestException(f"Request exception: {str(e)}")
        except Exception as e:
            Logger.error(f"An unexpected error occurred: {str(e)}", full_url)
            raise RequestUnhandleException(f"An unexpected error occurred: {str(e)}")