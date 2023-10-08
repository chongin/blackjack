from flask import Flask, request, jsonify

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
        player_name = request.args.get('player_name')
        game_data = {
            "table_name": table_name,
            "player_name": player_name,
        }
        return jsonify(game_data)

