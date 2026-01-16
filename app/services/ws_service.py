from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, thread_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[thread_id] = websocket
    
    def disconnect(self, thread_id: str):
        self.active_connections.pop(thread_id, None)
    
    async def send_message(self, thread_id: str, message: dict):
        websocket = self.active_connections.get(thread_id)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()