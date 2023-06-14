import time

from rich.console import Console
from websocket import create_connection

from learn_sql_model.config import get_config

config = get_config()
url = f"ws://{config.api_client.url.replace('https://', '')}/ws/heros"
Console().log(f"connecting to: {url}")
ws = create_connection(url)

data = []
while True:
    ws.send("hello".encode())
    time.sleep(1)
