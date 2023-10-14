
from importlib import import_module
import os
import re
from utils.util import Util
from api.messages.base_request import BaseRequest


class MessageFactory:
    def __init__(self) -> None:
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
    
    def find_message_file_name(self) -> list[str]:
        current_directory = Util.get_current_directory_of_file(__file__)
        messages_directory = current_directory + "/messages"
        message_files = []

        pattern = r'.*request\.py$'
        for filename in os.listdir(messages_directory):
            if re.match(pattern, filename):
                file_name_without_extension = os.path.splitext(filename)[0]
                message_files.append(file_name_without_extension)

        return message_files
