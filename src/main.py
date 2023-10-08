from servers.http_server import HttpServer
from message_factory import MessageFactory
from message_driver import MessageDriver

if __name__ == '__main__':
    MessageFactory.instance().regist_request('query_game')
    p = MessageFactory.instance().create_request('query_game', {"player_name": "abc", "table_name": "dd"})
    print(p)
    web_server = HttpServer(host='localhost', port=8080)
    web_server.run()
