from fastapi import FastAPI

from learn_sql_model.api.hero import hero_router
from learn_sql_model.api.user import user_router
from learn_sql_model.api.websocket import web_socket_router

# from fastapi_socketio import SocketManager


app = FastAPI()
# socket_manager = SocketManager(app=app)

app.include_router(hero_router)
app.include_router(user_router)
app.include_router(web_socket_router)


# @app.sio.on("join")
# def handle_join(sid, *args, **kwargs):
#     app.sio.emit("lobby", "User joined")


# @app.sio.on("leave")
# def handle_leave(sid, *args, **kwargs):
#     sm.emit("lobby", "User left")
