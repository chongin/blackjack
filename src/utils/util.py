
class Util:
    @classmethod
    def underscore_to_camelcase(self, name):
        return ''.join(word.capitalize() for word in name.split('_'))