import re
import os
from importlib import import_module
from utils.util import Util


class LoadFlowModules:
    def __init__(self) -> None:
        self.modules = {}
        self.import_flow_modules()

    def import_flow_modules(self):
        flow_file_names = self.find_flow_file_name()
        for flow_file_name in flow_file_names:
            module_name = f"business_logic.flow_control.{flow_file_name}"
            self.modules[flow_file_name] = import_module(module_name)

    def create_flow(self, name, job_data: dict) -> any:
        for flow_file_name, module in self.modules.items():
            if name in flow_file_name:
                try:
                    class_name = f"{Util.underscore_to_camelcase(flow_file_name)}"
                    class_ = getattr(module, f"{class_name}")
                    return class_(job_data)
                except AttributeError as ex:
                    print(str(ex))
                    break
        raise ValueError(f'Unknow flow: {name}')
    
    def find_flow_file_name(self) -> list[str]:
        current_directory = Util.get_current_directory_of_file(__file__)
        flow_directory = current_directory + "/../business_logic/flow_control"
        flow_files = []

        pattern = r'.*flow\.py$'
        for filename in os.listdir(flow_directory):
            if re.match(pattern, filename):
                file_name_without_extension = os.path.splitext(filename)[0]
                flow_files.append(file_name_without_extension)

        return flow_files