class ConnectionManager:
    #  TODO: for now, connections are represented as an in memory dictionary.
    # we will have to replace it in the future by a more robust solution (redis cache, for example)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
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
