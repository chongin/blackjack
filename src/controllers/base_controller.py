from abc import ABC, abstractmethod
class BaseController:
    def __init__(self, request) -> None:
        self.request = request

    @abstractmethod
    def handle_request(self) -> dict:
        pass