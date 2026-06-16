import os
from os.path import splitext, exists, join
import mimetypes
from pathlib import Path
from time import sleep
############# imports for watchdog below
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
######### Library used for moving files around
import shutil
from constants import audio_extensions, image_extensions, video_extensions, document_extensions
from Directory_Manager import DirectoryManager

source_dir = "C:\\Users\\Danny\\Downloads"
d_img = "C:\\Users\\Danny\\File_Management_test_folder\\Photos"
d_vid = "C:\\Users\\Danny\\File_Management_test_folder\\Videos"
d_exe = "C:\\Users\\Danny\\File_Management_test_folder\\Executables"
d_pdf = "C:\\Users\\Danny\\File_Management_test_folder\\Documents"
d_aud = "C:\\Users\\Danny\\File_Management_test_folder\\Audio"
d_other = "C:\\Users\\Danny\\File_Management_test_folder\\Other"


def make_unique(path, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{path}\\{name}"):
        name = f"{filename}({ str(counter) }){extension}"
        counter += 1

    return name



def move_file(dest, entry, name):
    try:
        file_exists = os.path.exists(dest + "\\" + name)

        if file_exists:
            unique_name = make_unique(dest, name)
            oldName = join(dest, name)
            newName = join(dest, unique_name)
            os.rename(oldName, newName)
        shutil.move(entry, dest)
    except Exception:
        print("An unknown error occurred, no changes were made")


class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):   #If there is a change detected in the source directory, this function is triggered and runs each function to move the file to the appropriate location
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                type = Path(name).suffix

                if type in document_extensions:
                    self.check_doc(entry, name)

                elif type in video_extensions:
                    self.check_video(entry, name)

                elif type in audio_extensions:
                    self.check_audio(entry, name)

                elif type in image_extensions:
                    self.check_image(entry, name)

                elif name.endswith(".exe"):
                    self.check_exe(entry, name)

                else:
                    self.move_to_other(entry, name, type)

    def check_audio(self, entry, name):
        dest = d_aud
        move_file(dest, entry, name)
        logging.info(f"Moved audio file: {name} from {source_dir} to {dest}")

    def check_image(self, entry, name):
        dest = d_img
        move_file(dest, entry, name)
        logging.info(f"Moved image file: {name} from {source_dir} to {dest}")


    def check_video(self, entry, name):
        dest = d_vid
        move_file(dest, entry, name)
        logging.info(f"Moved video file: {name} from {source_dir} to {dest}")

    def check_doc(self, entry, name):
        dest = d_pdf
        move_file(dest, entry, name)
        logging.info(f"Moved document file: {name} from {source_dir} to {dest}")

    def check_exe(self, entry, name):
        dest = d_exe
        move_file(dest, entry, name)
        logging.info(f"Moved executable file: {name} from {source_dir} to {dest}")

    def move_to_other(self, entry, name, type):
        dest = d_other
        move_file(dest, entry, name)
        logging.info(f"File type {type} was not recognized. Moved file: {name} from {source_dir} to {dest}")



#Below code is here now for ease of testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir #set the path you want here
    event_handler = MoveHandler() ##equate to the name of the class which moves the files. In this case it would be MoveHandler
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()