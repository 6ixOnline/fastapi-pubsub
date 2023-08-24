from abc import ABC, abstractmethod
from typing import Dict

import json

from fastapi import WebSocket, WebSocketDisconnect

from fastapi_pubsub.connection_manager import ConnectionManager


class BaseWebSocket(ABC):
    def __init__(self, websocket: WebSocket, websocket_id: str):
        self.websocket = websocket
        self.websocket_id = websocket_id
        self.connection_manager = ConnectionManager()

    async def send_json(self, data: Dict):
        await self.send_message(json.dumps(data))

    async def send_message(self, message: str):
        await self.websocket.send_text(message)

    async def receive_message(self) -> str:
        return await self.websocket.receive_text()

    async def close(self):
        await self.websocket.close()

    async def run(self, send_message_on_exception=True):
        await self.websocket.accept()
        self.connection_manager.add(self.websocket_id, self)

        try:
            for client in self.connection_manager.get(self.websocket_id):
                client.send_json(self.generate_object_to_send(client))

            while True:
                await self.websocket.receive_text()

        except WebSocketDisconnect:
            self.connection_manager.remove(self.websocket_id, self)

            if send_message_on_exception:
                for client in self.connection_manager.get(self.websocket_id):
                    client.send_json(self.generate_object_to_send(client))

    @abstractmethod
    async def generate_object_to_send(self):
        pass
