
from importlib import import_module
from typing import List
import os
import re
from utils.util import Util


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
        self.request_classes = {}
        self.modules = []
        message_names = self.find_message_file_name()

        for message_name in message_names:
            module_name = f"api.messages.{message_name}"
            self.modules.append(import_module(module_name))

    def regist_request(self, name) -> None:
        self.request_classes[name] = f"{Util.underscore_to_camelcase(name)}Request"

    def create_request(self, name, payload) -> any:
        for module in self.modules:
            class_ = getattr(module, f"{self.request_classes[name]}")
            print(class_)
            if name in self.request_classes:
                class_ = getattr(module, f"{self.request_classes[name]}")
                return class_(payload)
            else:
                raise ValueError(f'Unknow request: {name}')
    
    def find_message_file_name(self) -> List[str]:
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        messages_directory = current_directory + "/messages"
        message_files = []

        pattern = r'.*request\.py$'
        for filename in os.listdir(messages_directory):
            if re.match(pattern, filename):
                file_name_without_extension = os.path.splitext(filename)[0]
                message_files.append(file_name_without_extension)

        return message_files
