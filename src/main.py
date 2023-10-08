from servers.http_server import HttpServer
from api.message_factory import MessageFactory
from api.messages.query_game_request import QueryGameRequest

if __name__ == '__main__':
    MessageFactory.instance().regist_request('query_game')
    p = MessageFactory.instance().create_request('query_game', {"player_name": "abc", "table_name": "dd"})
    print(p)
    web_server = HttpServer(host='localhost', port=8080)
    web_server.run()
