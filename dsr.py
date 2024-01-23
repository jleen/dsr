import os
import sys
import time

from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd
        self.last = 0

    def on_any_event(self, event):
        if time.monotonic() > self.last + 0.1:  # HACK HACK HACK
            os.system(self.cmd)
            self.last = time.monotonic()


class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, addr, srv):
        super().__init__(req, addr, srv, directory=WebHandler.srv_dir)


[_, watch_dir, srv_dir, cmd] = sys.argv

def dsr():
    WebHandler.srv_dir = srv_dir

    observer = Observer()
    handler = WatchdogHandler(cmd)
    observer.schedule(handler, watch_dir, recursive=True)
    observer.start()

    try:
        httpd = HTTPServer(('', 8000), WebHandler)
        httpd.serve_forever()
    finally:
        observer.stop()
        observer.join
