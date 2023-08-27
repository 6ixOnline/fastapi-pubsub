from abc import ABC, abstractmethod
from typing import Dict

import json

from fastapi import WebSocket, WebSocketDisconnect

from fastapi_pubsub.connection_manager import MemoryConnectionManager, RedisConnectionManager


class RedisCredentials:
    host: str
    port: int
    username: str
    password: str
    db: int


class BasePubSubWebSocket(ABC):
    def __init__(self, websocket: WebSocket, websocket_id: str, redis_credentials: RedisCredentials = None):
        self.websocket = websocket
        self.websocket_id = websocket_id

        self.connection_manager = self._initialize_connection_manager(
            redis_credentials)

    def _initialize_connection_manager(self, redis_credentials: RedisCredentials):
        if redis_credentials is not None:
            return RedisConnectionManager(**redis_credentials.__dict__)
        else:
            return MemoryConnectionManager()

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
            await self.process()

            while True:
                await self.websocket.receive_text()

        except WebSocketDisconnect:
            self.connection_manager.remove(self.websocket_id, self)

            if send_message_on_exception:
                await self.process()

    async def process(self):
        for client in self.connection_manager.get(self.websocket_id):
            response = await self.generate_object_to_send()
            await client.send_json(response)

    @abstractmethod
    async def generate_object_to_send(self):
        pass
