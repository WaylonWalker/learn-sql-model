from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from learn_sql_model.api.websocket_connection_manager import manager

web_socket_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:5000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@web_socket_router.get("/watch")
async def get():
    return HTMLResponse(html)


@web_socket_router.websocket("/ws/{id}")
async def websocket_endpoint_connect(websocket: WebSocket, id: int):
    await manager.connect(websocket, id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[gold]You Said: {data}")
            await manager.broadcast(f"[blue]USER: {data}", id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, id)
        await manager.broadcast(f"Client #{id} left the chat", id)


@web_socket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"[blue]USER: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, id)
        await manager.broadcast(f"Client #{client_id} left the chat", id)
