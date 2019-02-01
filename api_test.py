from __future__ import print_function

import json
import threading
import time
import pprint

# pip install websocket-client
# !! NOT: pip install websocket
import websocket

URL = "ws://schuecobe5hackdays.azurewebsites.net/WebSocketServer.ashx?"

CONNECTION_REQUEST = {
    "type": "connection_request",
    "request_type": "connect_to_prop",
    "prop_id": 0
}

SET_VALUE = {
    "type": "set_value",
    "value_name": "ambient_temperature",
    "value": 10.0
}


class PropertyClient(object):
    def __init__(self, prop_id=0):
        self.prop_id = prop_id
        self.data = {}
        self.ws = websocket.WebSocketApp(
            URL,
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws))
        # Start run_forever() asynchronously to be non-blocking.
        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

    def wait_until_connected(self, timeout=5):
        # Stupid but YOLO
        while not self.ws.sock.connected and timeout:
            time.sleep(1)
            timeout -= 1

    def on_message(self, ws, message):
        payload = json.loads(message)
        if payload["type"] == "property_update":
            self.data.update({payload["value_name"]: payload["value"]})
            print(
                "Received an update, full data is now:",
                pprint.pformat(self.data),
                sep="\n")

    def on_error(self, ws, error):
        print("ERROR:", error)

    def on_close(self, ws):
        print("Socket closed!")

    def on_open(self, ws):
        def run(*args):
            request = CONNECTION_REQUEST
            request["prop_id"] = self.prop_id
            self.ws.send(json.dumps(request))

        thread = threading.Thread(target=run)
        thread.start()

    def set_value(self, value_name, value):
        request = SET_VALUE
        request["value_name"] = value_name
        request["value"] = value
        self.ws.send(json.dumps(request))


if __name__ == '__main__':
    websocket.enableTrace(True)

    # ID 0 would auto-assign a new number, we use 666 ;)
    prop = PropertyClient(prop_id=666)
    prop.wait_until_connected(timeout=10)

    while prop.ws.sock.connected:
        for i in range(3):
            prop.set_value("wind_speed", 10 * i)
            time.sleep(5)
