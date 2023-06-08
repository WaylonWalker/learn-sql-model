from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id: str):
        print("connecting...", id)
        if id not in self.active_connections:
            self.active_connections[id] = []
        await websocket.accept()
        self.active_connections[id].append(websocket)

    def disconnect(self, websocket: WebSocket, id: str):
        if id not in self.active_connections:
            return
        self.active_connections[id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, id: str):
        if id not in self.active_connections:
            return
        print(f"i go this message {message}")
        print(
            f"I am going to send it to {len(self.active_connections[id])} connections"
        )
        for connection in self.active_connections[id]:
            print("sending it to ", connection)
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection, id)
            print("sent it to ", connection)


manager = ConnectionManager()
