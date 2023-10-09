from abc import ABC, abstractmethod


class BaseController:
    def __init__(self, request) -> None:
        self.request = request

    @abstractmethod
    def handle_request(self) -> dict:
        pass
    
    def validate_request(self) -> bool:
        return True