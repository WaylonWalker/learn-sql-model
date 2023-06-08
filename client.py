import time

from rich.console import Console
from websocket import create_connection

from learn_sql_model.models.hero import Hero


def connect():
    id = 1
    url = f"ws://localhost:5000/ws/{id}"
    Console().log(f"connecting to: {url}")
    ws = create_connection(url)
    Console().log(f"connected to: {url}")
    return ws


data = []


def watch(ws):
    while ws.connected:
        try:
            data.append(ws.recv())
            if data[-1].startswith("{"):
                Console().log(Hero.parse_raw(data[-1]))
            else:
                Console().log(data[-1])
        except Exception as e:
            Console().log("failed to recieve data")
            Console().log(e)


if __name__ == "__main__":
    while True:
        try:
            ws = connect()
            watch(ws)
        except Exception as e:
            Console().log("failed to connect")
            Console().log(e)
            time.sleep(1)
