from fastapi import FastAPI, WebSocket

from fastapi_pubsub.base import BaseWebSocket


class SimpleWebsocket(BaseWebSocket):
    async def generate_object_to_send(self):
        connections = self.connection_manager.get(self.websocket_id)
        return {"num_connected_clients": len(connections)}


app = FastAPI()


@app.websocket("/ws/connected_clients")
async def online_players_endpoint(websocket: WebSocket):
    online_players_ws = SimpleWebsocket(websocket, 'connected_clients')
    await online_players_ws.run()
