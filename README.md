# FastAPI Pub/Sub

A simple but yet elegant publish/subscribe socket implementation using FastAPI Websocket.

## Installation

```
pip install fastapi-pubsub
```

## How it works

FastAPI provides an awesome implementation of Websockets. But it can be painful to configure it to work as a publish/subscribe mechanism.

FastAPI Pub/Sub implemented a `BaseWebSocket` that handles all client's connections under the hood. All you have to do is extend this class, overriding the method `generate_object_to_send(self)` with your desired logic.

```
from fastapi_pubsub.base import BaseWebSocket

class SimpleWebsocket(BaseWebSocket):
    async def generate_object_to_send(self):
        # any logic that you want to implement to send to connected users
        connections = self.connection_manager.get(self.websocket_id)
        return {"num_connected_clients": len(connections)}
```

```
app = FastAPI()

@app.websocket("/ws/connected_clients")
async def online_players_endpoint(websocket: WebSocket):
    ssw = SimpleWebsocket(websocket, 'connected_clients')
    await ssw.run()
```

A minimun example of a server/client communication can be seen [here.](https://github.com/dhiogocorrea/fastapi-pubsub/tree/main/examples) Follow the instructions to see it working.

## Contributing

Despite being full functional, this project is in a very early stage. **Pull requests are very welcome!**

In my opinion, a good next step here is to implement some in-memory database to store connections at [connection_manager](https://github.com/dhiogocorrea/fastapi-pubsub/blob/main/fastapi_pubsub/connection_manager.py). For now, it uses a dictionary to handle it.
