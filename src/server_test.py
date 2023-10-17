import asyncio
import websockets
import json
from logger import Logger
from utils.util import Util
from singleton_manger import SingletonManager


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected_clients = {}

    async def on_connect(self, websocket, path):
        client_id = id(websocket)
        Logger.info(f"Client: {client_id} connected to server, remote_addr: {websocket.remote_address}, path: {path}")

        try:
            async for message in websocket:
                data = json.loads(message)
                self._handle_message(client_id, websocket, data)
               
        except websockets.exceptions.ConnectionClosedError as ex:
            Logger.error("Client: {client_id} was closed", str(ex))
        finally:
            self._handle_disconnect(client_id)

    async def run(self):
        try:
            Logger.debug(f"Starting web server, host: {self.host}, {self.port}")
            async with websockets.serve(self.on_connect, self.host, self.port):
                await asyncio.Future()
        except KeyboardInterrupt:
            Logger.error("Receive KeyboardInterrupt, stop the web server")

    def _handle_message(self, client_id: int, websocket: any, data: dict) -> None:
        if self.connected_clients.get(client_id):
            SingletonManager.instance().connection_mgr.handle_message(data)
        else:
            if data.get('name') != 'Register':
                websocket.send("This client:{client_id} wasn't register yet, please register it first.")
            else:
                self.connected_clients[client_id] = Util.current_utc_time()
                resp = SingletonManager.instance().connection_mgr.handle_register()
                if resp != "OK":
                    websocket.send(resp)
                    websocket.close()
                    del self.connected_clients

    def _handle_disconnect(self, client_id):
        del self.connected_clients[client_id]
        SingletonManager.instance().connection_mgr.handle_disconnect(client_id)
        Logger.error(f"Client: {id} disconnected.")


if __name__ == "__main__":
    server = WebSocketServer("0.0.0.0", 8765)
    asyncio.run(server.run())
