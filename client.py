import time

from rich.console import Console
from websocket import create_connection

from learn_sql_model.config import get_config
from learn_sql_model.models.hero import Heros

config = get_config()


def connect():
    url = f"ws://{config.api_client.url.replace('https://', '')}/ws/heros"
    # url = f"ws://localhost:5000/ws/heros"
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
                # Console().log(data[-1])
                Console().log(Heros.parse_raw(data[-1]))
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
