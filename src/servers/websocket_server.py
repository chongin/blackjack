import asyncio
import websockets
import json
from logger import Logger
from utils.util import Util
from singleton_manger import SingletonManager

import json

class ResponseMsg:
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
    
    def to_dict(self):
        hash = {
            'code': self.code
        }

        if self.code != 'OK':
            hash['error_message'] = self.message
        else:
            hash['message'] = self.message
        return hash
    
    def to_json(self):
        return json.dumps(self.to_dict())


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
                await self._handle_message(client_id, websocket, data)
               
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

    async def _handle_message(self, client_id: int, websocket: any, data: dict) -> None:             
        if self.connected_clients.get(client_id):
            SingletonManager.instance().connection_mgr.handle_message(data)
        else:
            if data.get('name') != 'Register':
                error_rsp = ResponseMsg(
                    'error', 
                    "This client:{client_id} wasn't register yet, please register it first."
                ).to_json()
                await websocket.send(error_rsp)
                await websocket.close()
            else:
                self.connected_clients[client_id] = Util.current_utc_time()
                data.update({
                    'client_id': client_id,
                    'websocket': websocket
                })
                resp = SingletonManager.instance().connection_mgr.handle_register(data)
                if resp != "OK":
                    error_rsp = ResponseMsg('error', resp).to_json()
                    await websocket.send(error_rsp)
                    await websocket.close()
                    del self.connected_clients[client_id]
                else:
                    resp = ResponseMsg('OK', "Handle Register success.").to_json()
                    await websocket.send(resp)

    def _handle_disconnect(self, client_id):
        websocket = self.connected_clients.get(client_id)
        if not websocket:
            Logger.error("Cannot find this client from webserver memory, cannot handle disconnect.")
            return
        del websocket
        SingletonManager.instance().connection_mgr.handle_disconnect(client_id)
        Logger.debug(f"Client: {id} disconnected.")


# if __name__ == "__main__":
#     server = WebSocketServer("0.0.0.0", 8765)
#     asyncio.run(server.run())
