class SystemException(Exception):
    def __init__(self, error_code, err_message):
        self.error_code = error_code
        self.err_message = err_message
        self.name = self.get_name()
        super().__init__(f"Error Code: {error_code}, Message: {err_message}")

    def to_hash(self):
        return {
            "name": self.name,
            "error_code": self.error_code,
            "err_message": self.err_message
        }

    def get_name(self):
        class_name = self.__class__.__name__
        formatted_name = ""
        for char in class_name:
            if char.isupper() and formatted_name:
                formatted_name += " "
            formatted_name += char
        return formatted_name