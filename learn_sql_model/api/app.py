from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from learn_sql_model.api.hero import hero_router
from learn_sql_model.api.user import user_router
from learn_sql_model.api.websocket import web_socket_router

app = FastAPI()

app.include_router(hero_router)
app.include_router(user_router)
app.include_router(web_socket_router)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Learn SQL Model</title>
    </head>
    <body>
        <h1>Learn SQL Model</h1>
        <p>Join the game with the following command.
        </p>
        <p>
        pipx run --spec git+https://github.com/WaylonWalker/learn-sql-model lsm game run
        </p>
        <p>
        You can watch player data at <a href='/watch'>watch</a>
        </p>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
