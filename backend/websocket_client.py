import websocket, ssl, time, json, threading

class WebsocketClient:

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.ws = None
        self.is_running = True

    def start(self):
        threading.Thread(target=self._connection_manager, daemon=True).start()

    def _connection_manager(self):
        while self.is_running:
            if self.ws is None:
                try:
                    self.ws = websocket.create_connection(
                        self.url,
                        header={"Authorization": self.token},
                        sslopt={"cert_reqs": ssl.CERT_NONE}
                    )
                    print("Status: Connected")
                except:
                    self.ws = None
                    print("Status: Connection failed, retrying...")
                    time.sleep(5)
            else:
                try:
                    self.ws.ping()
                except:
                    self.ws = None
                time.sleep(2)

    def send_message(self, text, magnitude, msg_type):
        if self.ws is None:
            return "no connection"

        payload = {
            "text": text,
            "magnitude": magnitude,
            "type": msg_type
        }

        try:
            self.ws.send(json.dumps(payload))
            response = self.ws.recv()
            return response
        except:
            self.ws = None
            return "no connection"
