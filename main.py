import sys
import os
import time
# Add the parent directory (src) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './src')))

from servers.http_server import HttpServer
from servers.websocket_server import WebSocketServer
from singleton_manger import SingletonManager
from configuration.system_config import SystemConfig
import asyncio
import threading

from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route and its corresponding function
@app.route('/')
def home():
    return 'Hello, World!'


if __name__ == '__main__':
    # start job manager to handle the game flow
    SingletonManager.instance().message_factory
    SingletonManager.instance().job_mgr.start_timer()
    SystemConfig.instance().set_tables()

    print("000000000000000000")
    # start web server to handle client request for client easily to handle timeout
    # or maybe later can accept other service api call.
    http_server = HttpServer(host='0.0.0.0', port=8080)
    thread = threading.Thread(target=app.run)
    thread.start()
    print("111111111111111111")
    # start the web server to handle cient connection for pushing message to client
    websocket_server = WebSocketServer('0.0.0.0', 8000)
    print("22222222222222222")
    asyncio.run(websocket_server.run())
    print("3333333333333")

