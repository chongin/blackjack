from servers.http_server import HttpServer
from servers.web_socket_server import WebSocketServer
from singleton_manger import SingletonManager
from message_factory import MessageFactory

if __name__ == '__main__':
    # start job manager to handle the game flow
    MessageFactory.instance()
    SingletonManager.instance().job_mgr
    
    # start the web server to handle cient connection for pushing message to client
    # ### WebSocketServer().run()

    # start web server to handle client request for client easily to handle timeout
    # or maybe later can accept other service api call.
    web_server = HttpServer(host='localhost', port=8080)
    web_server.run()
