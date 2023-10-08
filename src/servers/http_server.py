from flask import Flask, request, jsonify
from message_driver import MessageDriver
app = Flask(__name__)


class HttpServer:
    def __init__(self, host, port) -> None:
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()

    def setup_routes(self) -> None:
        self.app.route('/api/tables/<table_name>/query_game', methods=["GET"])(
            self.query_game
        )

    def run(self) -> None:
        self.app.run(host=self.host, port=self.port)

    def query_game(self, table_name: str) -> str:
        message_data = {
            "action": "query_game",
            "table_name": table_name,
            "player_name": request.args.get('player_name'),
        }

        response = MessageDriver(message_data).process_message()
        return jsonify(response)

