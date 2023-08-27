# FastAPI Pub/Sub

A simple but yet elegant publish/subscribe socket implementation using FastAPI Websocket.

## Installation

```
pip install fastapi-pubsub
```

## How it works

FastAPI provides an awesome implementation of Websockets. But it can be painful to configure it to work as a publish/subscribe mechanism.

FastAPI Pub/Sub implemented a `BasePubSubWebSocket` that handles all client's connections under the hood. All you have to do is extend this class, overriding the method `generate_object_to_send(self)` with your desired logic.

```python
from fastapi_pubsub import BasePubSubWebSocket

class SimplePubSubWebsocket(BasePubSubWebSocket):
    async def generate_object_to_send(self):
        # any logic that you want to implement to send to connected users
        connections = self.connection_manager.get(self.websocket_id)
        return {"num_connected_clients": len(connections)}
```

```python
app = FastAPI()

@app.websocket("/ws/connected_clients")
async def online_players_endpoint(websocket: WebSocket):
    ssw = SimplePubSubWebsocket(websocket, 'connected_clients')
    await ssw.run()
```

### BasePubSubWebSocket constructor parameters

|   Parameter   |   Mandatory   |   Default |   Description |
|:-------------|:-------------|:---------|:-------------|
|   websocket   |   yes         |   -       |   the fastapi websocket instance
|   channel_id  |   yes         |   -       | a custom unique id that identifies that operation. used by connection manager to group clients connected in the same channel
|   redis_credentials   |   no  |   None. if not passed, uses the [dict in-memory](https://github.com/6ixOnline/fastapi-pubsub/blob/main/fastapi_pubsub/connection_manager.py#L20) implementation    | redis host, port, username, password and db configuration  

---

A minimum example of a server/client communication can be seen [here.](https://github.com/dhiogocorrea/fastapi-pubsub/tree/main/examples) Follow the instructions to see it working.

## Contributing

Despite being full functional, this project is in a very early stage. **Pull requests are very welcome!**
