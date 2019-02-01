from __future__ import print_function

import json

# pip install websocket-client
# !! NOT: pip install websocket
import websocket

URL = "ws://schuecobe5hackdays.azurewebsites.net/WebSocketServer.ashx?"

if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect(URL)
    data = {
        "type": "connection_request",
        "request_type": "connect_to_prop",
        "prop_id": 0
    }
    ws.send(json.dumps(data))
    response = ws.recv()
    print(response)
    data = json.loads(response)
    print("I received value: ", data["value"])
