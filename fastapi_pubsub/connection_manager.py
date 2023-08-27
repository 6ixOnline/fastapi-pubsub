from abc import ABC, abstractmethod
from typing import Any
import redis


class BaseConnectionManager(ABC):
    @abstractmethod
    def get(self, channel_id: str):
        pass

    @abstractmethod
    def add(self, channel_id: str, value: Any):
        pass

    @abstractmethod
    def remove(self, channel_id: str, value: Any):
        pass


class MemoryConnectionManager(BaseConnectionManager):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryConnectionManager, cls).__new__(cls)
            cls._instance.connections = {}
        return cls._instance

    def get(self, channel_id: str):
        return self.connections.get(channel_id, set())

    def add(self, channel_id: str, value: Any):
        if channel_id not in self.connections:
            self.connections[channel_id] = set()

        self.connections[channel_id].add(value)

    def remove(self, channel_id: str, value: Any):
        connections_set = self.connections.get(channel_id)
        if connections_set:
            connections_set.remove(value)


class RedisConnectionManager:
    def __init__(self, host: str, port: int, username: str, password: str, db: int):
        self.storage = redis.StrictRedis(
            host=host, port=port, db=db, username=username, password=password)

    def get(self, channel_id: str):
        connections = self.storage.smembers(channel_id)
        return set(connections)

    def add(self, channel_id: str, value: Any):
        self.storage.sadd(channel_id, value)

    def remove(self, channel_id: str, value: Any):
        self.storage.srem(channel_id, value)
