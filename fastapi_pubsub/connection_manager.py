from abc import ABC, abstractmethod
from typing import Any
import redis


class BaseConnectionManager(ABC):
    @abstractmethod
    def get(self, websocket_id: str):
        pass

    @abstractmethod
    def add(self, websocket_id: str, value: Any):
        pass

    @abstractmethod
    def remove(self, websocket_id: str, value: Any):
        pass


class MemoryConnectionManager(BaseConnectionManager):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryConnectionManager, cls).__new__(cls)
            cls._instance.connections = {}
        return cls._instance

    def get(self, websocket_id: str):
        return self.connections.get(websocket_id, set())

    def add(self, websocket_id: str, value: Any):
        if websocket_id not in self.connections:
            self.connections[websocket_id] = set()

        self.connections[websocket_id].add(value)

    def remove(self, websocket_id: str, value: Any):
        connections_set = self.connections.get(websocket_id)
        if connections_set:
            connections_set.remove(value)


class RedisConnectionManager:
    def __init__(self, host: str, port: int, username: str, password: str, db: int):
        self.storage = redis.StrictRedis(
            host=host, port=port, db=db, username=username, password=password)

    def get(self, websocket_id: str):
        connections = self.storage.smembers(websocket_id)
        return set(connections)

    def add(self, websocket_id: str, value: Any):
        self.storage.sadd(websocket_id, value)

    def remove(self, websocket_id: str, value: Any):
        self.storage.srem(websocket_id, value)
