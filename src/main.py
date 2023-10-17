from servers.http_server import HttpServer
from servers.websocket_server import WebSocketServer
from singleton_manger import SingletonManager
from configuration.system_config import SystemConfig
import asyncio
import threading

if __name__ == '__main__':
    # start job manager to handle the game flow
    SingletonManager.instance().message_factory
    SingletonManager.instance().job_mgr.start_timer()
    SystemConfig.instance().set_tables()

    # start web server to handle client request for client easily to handle timeout
    # or maybe later can accept other service api call.
    http_server = HttpServer(host='localhost', port=8080)
    thread = threading.Thread(target=http_server.run)
    thread.start()
    # start the web server to handle cient connection for pushing message to client
    websocket_server = WebSocketServer('127.0.0.1', 8000)
    asyncio.run(websocket_server.run())

