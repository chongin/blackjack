import os
from datetime import datetime
import re

class Util:
    @classmethod
    def underscore_to_camelcase(cls, name: str) -> str:
        return ''.join(word.capitalize() for word in name.split('_'))

    #  transform BetStarted to bet_started
    @classmethod 
    def camelcase_to_underscore(cls, name: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    
    @classmethod
    def get_current_directory_of_file(cls, file: str) -> str:
        current_script_path = os.path.abspath(file)
        current_directory = os.path.dirname(current_script_path)
        return current_directory

    @classmethod
    def current_utc_time(cls) -> str:
        current_utc_time = datetime.utcnow()
        return current_utc_time.strftime('%Y-%m-%dT%H:%M:%S')
