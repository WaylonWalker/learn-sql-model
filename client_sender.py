import time

from rich.console import Console
from websocket import create_connection

id = 1
url = f"ws://localhost:5000/ws/{id}"
Console().log(f"connecting to: {url}")
ws = create_connection(url)

data = []
while True:
    ws.send("hello".encode())
    time.sleep(1)
