from __future__ import print_function

try:
    import thread
except ImportError:
    import _thread as thread
import json
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


class PropertyClient(object):
    def __init__(self, prop_id=0):
        self.prop_id = prop_id
        self.data = {}
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            URL,
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws))

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
            connection_request = CONNECTION_REQUEST
            connection_request["prop_id"] = self.prop_id
            self.ws.send(json.dumps(CONNECTION_REQUEST))

        thread.start_new_thread(run, ())


if __name__ == '__main__':
    prop = PropertyClient(prop_id=0)
    prop.ws.run_forever()
