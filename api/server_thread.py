import time
from threading import Thread
from flask import Flask
from werkzeug.serving import make_server


class ServerThread(Thread):
    """Class managing the thread of the API."""
    def __init__(self, app: Flask, host: str="0.0.0.0", port: int=8000):
        Thread.__init__(self)
        self.server = make_server(host, port, app, threaded=True)
        self.ctx = app.app_context()
        self.ctx.push()

        self.running = False

    def run(self):
        """Initialize the GUI thread."""
        if not self.running:
            self.server.serve_forever()
            self.running = True
        time.sleep(10)

    def shutdown(self):
        """Stop the GUI thread."""
        self.server.shutdown()
        self.running = False
        super().join()