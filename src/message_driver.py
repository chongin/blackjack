
import json
import traceback
from exceptions.system_exception import *
from message_factory import MessageFactory
from api.messages.base_request import BaseRequest
from controller_factory import ControllerFactory

class MessageDriver:
    def __init__(self, payload):
        self.payload = payload

    def process_message(self):
        try:
            request = self._build_message(self.payload)
            controller = self._build_controller(request)
           # response_hash = controller.handle_request()
            print(controller)
        except SystemException as e:
            return json.dumps(e.to_hash())
        except Exception as e:
            error_messsage = e.args[0]
            traceback.print_exc()
            return json.dumps({"error_code": 500, "error_message": error_messsage})

    def _build_message(self, payload) -> BaseRequest:
        return MessageFactory.instance().create_request(
            payload.get('action'), payload
        )

    def _build_controller(self, request):
        return ControllerFactory.instance().create_controller(request)
