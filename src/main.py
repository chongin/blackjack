from servers.http_server import HttpServer
from servers.web_socket_server import WebSocketServer
from job_system.job_manager import JobManager


if __name__ == '__main__':
    # start job manager to handle the game flow
    JobManager.instance().start_timer()

    # start the web server to handle cient connection for pushing message to client
    # ### WebSocketServer().run()

    # start web server to handle client request for client easily to handle timeout
    # or maybe later can accept other service api call.
    web_server = HttpServer(host='localhost', port=8080)
    web_server.run()
