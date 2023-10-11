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
            self.handle_query_game
        )

        self.app.route('/api/tables/<table_name>/players/<player_name>/bet', methods=["POST"])(
            self.handle_bet
        )

        self.app.route('/api/tables/<table_name>/players/<player_name>/hit', methods=["POST"])(
            self.handle_hit
        )

    def run(self) -> None:
        self.app.run(host=self.host, port=self.port)

    def handle_query_game(self, table_name: str) -> str:
        message_data = {
            "action": "query_game",
            "table_name": table_name,
            "player_name": request.args.get('player_name'),
        }

        response = MessageDriver(message_data).process_message()
        return jsonify(response)

    def handle_bet(self, table_name: str, player_name: str) -> str:
        data = request.get_json()
        message_data = {
            "action": "bet",
            "table_name": table_name,
            "player_name": player_name,
            "round_id": data.get('round_id'),
            "bet_options": data.get('bet_options')
        }

        response = MessageDriver(message_data).process_message()
        return jsonify(response)
    
    def handle_hit(self, table_name: str, player_name: str) -> str:
        data = request.get_json()
        message_data = {
            "action": "hit",
            "table_name": table_name,
            "player_name": player_name,
            "round_id": data.get('round_id')
        }

        response = MessageDriver(message_data).process_message()
        return jsonify(response)