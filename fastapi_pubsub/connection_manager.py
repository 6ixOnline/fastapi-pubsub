from abc import ABC, abstractmethod
import redis


class BaseConnectionManager(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def add(self, key, obj):
        pass

    @abstractmethod
    def remove(self, key, obj):
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

    def add(self, websocket_id: str, obj):
        if websocket_id not in self.connections:
            self.connections[websocket_id] = set()

        self.connections[websocket_id].add(obj)

    def remove(self, websocket_id: str, obj):
        connections_set = self.connections.get(websocket_id)
        if connections_set:
            connections_set.remove(obj)


class RedisConnectionManager:
    def __init__(self, host: str, port: int, username: str, password: str, db: int):
        self.storage = redis.StrictRedis(
            host=host, port=port, db=db, username=username, password=password)

    def get(self, key):
        connections = self.storage.smembers(key)
        return set(connections)

    def add(self, key, obj):
        self.storage.sadd(key, obj)

    def remove(self, key, obj):
        self.storage.srem(key, obj)
