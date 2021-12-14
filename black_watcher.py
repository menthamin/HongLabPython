# Written by Jeong-Mo Hong

import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FormatEventHandler(FileSystemEventHandler):
    def __init__(self, logger=None):
        super().__init__()

    def update_ipynb(self, event):
        if not event.is_directory and event.src_path.endswith("ipynb"):
            os.system("black " + event.src_path)

    def on_created(self, event):
        super().on_created(event)
        self.update_ipynb(event)

    def on_modified(self, event):
        super().on_modified(event)
        self.update_ipynb(event)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    event_handler = FormatEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("Start watchdog")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
