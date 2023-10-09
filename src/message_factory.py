
from importlib import import_module
from typing import List
import os
import re
from utils.util import Util
from api.messages.base_request import BaseRequest

class MessageFactory:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance

    def __init_manual__(self) -> None:
        self.modules = {}
        message_file_names = self.find_message_file_name()

        for message_file_name in message_file_names:
            module_name = f"api.messages.{message_file_name}"
            self.modules[message_file_name] = import_module(module_name)

    def create_request(self, name, payload) -> BaseRequest:
        for message_file_name, module in self.modules.items():
            if name in message_file_name:
                try:
                    class_name = f"{Util.underscore_to_camelcase(message_file_name)}"
                    class_ = getattr(module, f"{class_name}")
                    return class_(payload)
                except AttributeError as ex:
                    print(str(ex))
                    break
        raise ValueError(f'Unknow request: {name}')
    
    def find_message_file_name(self) -> List[str]:
        current_directory = Util.get_current_directory_of_file(__file__)
        messages_directory = current_directory + "/api/messages"
        message_files = []

        pattern = r'.*request\.py$'
        for filename in os.listdir(messages_directory):
            if re.match(pattern, filename):
                file_name_without_extension = os.path.splitext(filename)[0]
                message_files.append(file_name_without_extension)

        return message_files
