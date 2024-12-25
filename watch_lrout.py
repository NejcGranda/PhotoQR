import os
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import time
import common
import publish
import threading

# Load environment variables from .env file
load_dotenv()

LR_OUT_PATH = os.getenv('LIGHTROOM_OUT_FOLDER')
DESTINATION_FOLDER = os.getenv('PUBLISH_FOLDER')
TIME_THRESHOLD = 10

class LROutFolderHandler(FileSystemEventHandler):

    timer = None

    def __init__(self):
        self.timer = None

    def on_created(self, event):
        print(f"Event type: {event.event_type}, path: {event.src_path}")
        if self.timer is not None:
            self.timer.cancel()

        # Start the timer
        print(f"Starting timer for {TIME_THRESHOLD} seconds... at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.timer = threading.Timer(TIME_THRESHOLD, self.move_files)
        self.timer.start()

    def move_files(self):
        print(f"Moving files to destination folder... at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        publish.move_resize_and_zip_images(os.getenv('LIGHTROOM_OUT_FOLDER'), os.getenv('PUBLISH_FOLDER'))

        # Run sync.sh script to sync the PUBLISH_FOLDER with the server
        print("Syncing with the server...")
        subprocess.run(["./sync.sh"])
    
if __name__ == "__main__":
    # Check that the destination folder exists
    if not os.path.exists(DESTINATION_FOLDER):
        print(f"Destination folder does not exist: {DESTINATION_FOLDER}")
        exit(1)

    # Watch the LR Output directory for changes
    observer = Observer()
    handler = LROutFolderHandler()
    observer.schedule(handler, path=LR_OUT_PATH, recursive=False)

    print("Monitoring for Lightroom Out folder chnages...")
    try:
        observer.start()
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
