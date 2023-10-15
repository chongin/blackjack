from servers.http_server import HttpServer
from servers.web_socket_server import WebSocketServer
from singleton_manger import SingletonManager
from configuration.system_config import SystemConfig

if __name__ == '__main__':
    # start job manager to handle the game flow
    SingletonManager.instance().message_factory
    SingletonManager.instance().job_mgr
    SystemConfig.instance().set_tables()
    # start the web server to handle cient connection for pushing message to client
    # ### WebSocketServer().run()

    # start web server to handle client request for client easily to handle timeout
    # or maybe later can accept other service api call.
    web_server = HttpServer(host='localhost', port=8080)
    web_server.run()
