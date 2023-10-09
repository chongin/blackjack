from controllers.base_controller import BaseController
from importlib import import_module
from typing import List
import os
import re
from utils.util import Util
from api.messages.base_request import BaseRequest


class ControllerFactory:
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
        self.controller_classes = {}
        self.modules = {}
        controlller_file_names = self.find_controller_file_name()

        for controller_file_name in controlller_file_names:
            module_name = f"controllers.{controller_file_name}"
            self.modules[controller_file_name] = import_module(module_name)
    
    def create_controller(self, request: BaseRequest) -> BaseController:
        for controller_file_name, module in self.modules.items():
            if request.action in controller_file_name:
                try:
                    class_name = f"{Util.underscore_to_camelcase(controller_file_name)}"
                    class_ = getattr(module, class_name)
                    return class_(request)
                except AttributeError as ex:
                    print(str(ex))
                    break
            
        return ValueError(f'Unknow handler: {request.action}')
    
    def find_controller_file_name(self) -> List[str]:
        current_directory = Util.get_current_directory_of_file(__file__)
        controllers_directory = current_directory + "/controllers"
        controller_files = []

        pattern = r'.*controller\.py$'
        for filename in os.listdir(controllers_directory):
            if re.match(pattern, filename):
                file_name_without_extension = os.path.splitext(filename)[0]
                controller_files.append(file_name_without_extension)

        return controller_files