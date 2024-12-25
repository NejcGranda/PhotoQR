import os
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import time
import common

# Load environment variables from .env file
load_dotenv()

# Define the SD card's mount point and the destination folder
SD_CARD_PATH = "/Volumes/EOS_DIGITAL"
DESTINATION_FOLDER = os.getenv('LIGHTROOM_IN_FOLDER')

class SDCardHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Any Event. Type: {event.event_type}, path: {event.src_path}")

    def on_modified(self, event):
        print(f"Event type: {event.event_type}, path: {event.src_path}")
        # Check if the SD card is mounted
        if os.path.exists(SD_CARD_PATH):
            print(f"SD card detected: {SD_CARD_PATH}")
            # Sleep 5s to ensure the SD card is mounted properly
            print("Waiting for the SD card to mount... (5s)")
            time.sleep(5)
            self.move_files_flat()
            self.unmount_sd_card()

    def move_files_flat(self):

        code = common.pick_the_code()
        print(f"Selected code: {code}")

        print("Moving files to destination folder...")
        try:
            # Traverse all files in the SD card, including subdirectories
            for root, dirs, files in os.walk(SD_CARD_PATH, topdown=False):
                print(f"Processing folder: {root}")
                print(f"Files: {files}")
                for file in files:
                    print(f"File: {file}")
                    source_path = os.path.join(root, file)

                    # Check if the file is an image: JPG, JPEG, RAF, CR2
                    if not file.lower().endswith((".jpg", ".jpeg", ".raf", ".cr2")):
                        print(f"Skipping, not an image file: {file}")
                        continue

                    destination_path = os.path.join(DESTINATION_FOLDER, f"{code}_{file}")
                    
                    # Ensure no filename conflicts by renaming duplicates
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(destination_path):
                            new_name = f"{base}_{counter}{ext}"
                            destination_path = os.path.join(DESTINATION_FOLDER, new_name)
                            counter += 1
                    
                    shutil.move(source_path, destination_path)
                    # shutil.copy(source_path, destination_path)

            # Print new empty line
            print()
            print("*" * 20)
            print(f"All files moved to {DESTINATION_FOLDER} (flat structure) at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            print(f"Code: {code}")
            print()
            print("*" * 20)
        except Exception as e:
            print(f"Error while moving files: {e}")

    def unmount_sd_card(self):
        try:
            # Unmount the SD card using diskutil
            subprocess.run(["diskutil", "unmount", SD_CARD_PATH], check=True)
            print(f"SD card {SD_CARD_PATH} successfully unmounted.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to unmount SD card: {e}")

if __name__ == "__main__":
    # Check that the destination folder exists
    if not os.path.exists(DESTINATION_FOLDER):
        print(f"Destination folder does not exist: {DESTINATION_FOLDER}")
        exit(1)

    # Watch the /Volumes directory for changes
    observer = Observer()
    handler = SDCardHandler()
    observer.schedule(handler, path="/Volumes", recursive=False)

    print("Monitoring for SD card insertion...")
    try:
        observer.start()
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
