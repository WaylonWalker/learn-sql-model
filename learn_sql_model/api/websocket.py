from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from rich.console import Console
from sqlmodel import Session
from websockets.exceptions import ConnectionClosed

from learn_sql_model.api.websocket_connection_manager import manager
from learn_sql_model.config import get_session
from learn_sql_model.console import console
from learn_sql_model.models.hero import HeroDelete, HeroUpdate, Heros

web_socket_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Heros Stream</h1>
        <code id='messages'>
        </code>
        <script>
            var ws = new WebSocket("wss://learn-sql-model.fly.dev/ws/heros");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                messages.innerHTML = event.data
            };
        </script>
    </body>
</html>
"""


@web_socket_router.get("/watch")
async def get():
    return HTMLResponse(html)


@web_socket_router.websocket("/ws/{channel}")
async def websocket_endpoint_connect(
    websocket: WebSocket,
    channel: str,
    session: Session = Depends(get_session),
):
    Console().log(f"Client #{id} connecting")
    await manager.connect(websocket, channel)
    heros = Heros.list(session=session)
    await websocket.send_text(heros.json())

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket, id)
        await manager.broadcast(f"Client #{channel} left the chat", channel)


@web_socket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"[blue]USER: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, id)
        await manager.broadcast(f"Client #{id} left the chat", id)


@web_socket_router.websocket("/wsecho")
async def websocket_endpoint_hero_echo(
    websocket: WebSocket,
    session: Session = Depends(get_session),
):
    await websocket.accept()
    last_heros = None

    try:
        while True:
            data = await websocket.receive_text()
            hero = HeroUpdate.parse_raw(data)
            heros = Heros.list(session=session)
            if heros != last_heros:
                await manager.broadcast(heros.json(), "heros")
                last_heros = heros
            hero.update(session=session)
            console.print(heros)
            await websocket.send_text(heros.json())

    except WebSocketDisconnect:
        try:
            HeroDelete(id=hero.id).delete(session=session)
        except Exception:
            ...
        heros = Heros.list(session=session)
        await manager.broadcast(heros.json(), "heros")
        print("disconnected")
    except ConnectionClosed:
        try:
            HeroDelete(id=hero.id).delete(session=session)
        except Exception:
            ...
        heros = Heros.list(session=session)
        await manager.broadcast(heros.json(), "heros")
        print("connection closed")
