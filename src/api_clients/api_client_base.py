import requests


class ApiClientBase:
    def __init__(self, endpoint, timeout=10):
        self.endpoint = endpoint
        self.timeout = timeout

    def make_request(self, url_suffix, method="GET", data=None):
        full_url = f"{self.endpoint}/{url_suffix}"
        try:
            if method == "GET":
                response = requests.get(full_url, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(full_url, json=data, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
            return response.json()
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None