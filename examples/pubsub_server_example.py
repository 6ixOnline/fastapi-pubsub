from fastapi import FastAPI, WebSocket

from fastapi_pubsub import BasePubSubWebSocket


class SimplePubSubWebsocket(BasePubSubWebSocket):
    async def generate_object_to_send(self):
        connections = self.connection_manager.get(self.channel_id)
        return {"num_connected_clients": len(connections)}


app = FastAPI()


@app.websocket("/ws/connected_clients")
async def online_players_endpoint(websocket: WebSocket):
    online_clients_ws = SimplePubSubWebsocket(
        websocket=websocket, channel_id='connected_clients')
    await online_clients_ws.run()
