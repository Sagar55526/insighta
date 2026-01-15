from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, message_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[message_id] = websocket
    
    def disconnect(self, message_id: str):
        self.active_connections.pop(message_id, None)
    
    async def send_message(self, message_id: str, message: dict):
        websocket = self.active_connections.get(message_id)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()