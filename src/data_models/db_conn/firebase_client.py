import firebase_admin
from firebase_admin import credentials, db
from utils.util import Util


class FirebaseClient:
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
        database_url = 'https://blackjack-881c3-default-rtdb.firebaseio.com/'
        service_account_key_path = Util.get_current_directory_of_file(__file__)
        service_account_key_path += "/service_account_key.json"
        self.cred = credentials.Certificate(service_account_key_path)
        firebase_admin.initialize_app(self.cred, {'databaseURL': database_url})
        self.db_root_ref = db.reference()  # ref to the root of database

    def get_value(self, path: str) -> dict:
        return self.db_root_ref.child(path).get()

    def set_value(self, path, value) -> None:
        self.db_root_ref.child(path).set(value)

