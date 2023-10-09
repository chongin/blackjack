import os


class Util:
    @classmethod
    def underscore_to_camelcase(self, name: str) -> str:
        return ''.join(word.capitalize() for word in name.split('_'))

    @classmethod
    def get_current_directory_of_file(self, file: str) -> str:
        current_script_path = os.path.abspath(file)
        current_directory = os.path.dirname(current_script_path)
        return current_directory
