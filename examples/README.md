# FastAPI Pub/Sub - Examples

## Server:

This server extends the base class `BaseWebSocket` and implements the `generate_object_to_send` method by simply sending the number of connected clients each time a new client is connected to this websocket url.

### Running:

Simply run the uvicorn server:

```
uvicorn pubsub_server_example:app
```

And now you are good to go to the client.

## Client

This client uses `asyncio` to connect to the server to start listening to messages. You can try to start several clients by running:

```
python3 pubsub_client_example.py
```

And you will see that each time a new client connects or disconnects, every connected client receives a message.
