import os
from os.path import splitext, exists, join
from time import sleep
############# imports for watchdog below
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
######### Library used for moving files around
import shutil

source_dir = "C:\\Users\\Danny\\Downloads"
d_pho = "C:\\Users\\Danny\\Pictures\\Saved Pictures"
d_vid = "C:\\Users\\Danny\\Pictures\\Saved Pictures"
d_exe = "C:\\Users\\Danny\\Documents\\exe"
d_pdf = "C:\\Users\\Danny\\Documents\\pdf"
d_aud = "C:\\Users\\Danny\\Music\\Audio"
d_other = "C:\\Users\\Danny\\Downloads"


# supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]



class Directory_Manager():
    def __init__(self, path):
        self.startpath = path
        self.dir_map = {}
        self.file_map = {}
        self.sorted_map = {}

        with os.scandir(self.startpath) as files:
            i = 0
            for entry in files:
                if entry.is_file():
                    self.file_map["File|  Index: " + str(i)] = entry.name

                if entry.is_dir():
                    self.dir_map["Folder| Index: " + str(i)] = entry.name

                i += 1

        for item in self.dir_map.items():
            self.sorted_map[item[0]] = item[1]


        for entry in self.file_map.items():
            self.sorted_map[entry[0]] = entry[1]


    def listfiles(self):
        if not self.file_map:
            return "There are no files"
        else:
            for item in self.file_map.items():
                print(item)

    def listDir(self):
        if not self.dir_map:
            return "There are no folders"
        else:
            for item in self.dir_map.items():
                print(item)

    def listall(self):
        if self.sorted_map:
            for item in sorted(self.sorted_map.items()):
                print(item)
#####################################################
def make_name(path, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{path}\\{name}"):
        name = f"{filename}({ str(counter) }){extension}"

    return name



def move_file(dest, entry, name): #Needs work

    DM = Directory_Manager(dest)

    if entry not in DM.file_map or entry not in DM.dir_map:
        shutil.move(entry, dest)



    # if not exists(f"{dest}\\{name}"): #Checks if a file already exists then renames it if it does
    #     # unique_name = make_name(dest, name)
        # oldname = join(dest, name)
        # newname = join(dest, unique_name)
        # os.rename(oldname, newname)




class MoveHandler(FileSystemEventHandler):
    def check_audio(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000:
                    dest = d_aud
                else:
                    dest = d_other
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_image(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension):
                move_file(d_pho, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_video(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(d_vid, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_doc(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(d_pdf, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_exe(self, entry, name):
        if name.endswith(".exe"):
            move_file(d_exe, entry, name)
            logging.info(f"Moved executable file: {name}")

    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_doc(entry, name)
                self.check_exe(entry, name)
                self.check_video(entry, name)
                self.check_audio(entry, name)
                self.check_image(entry, name)







#####################################################
#using Watchdog here


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
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

###############################################






######
# start_path = 'C:\\Users\\Danny\\Documents'
#
# dir_map = {}
# file_map = {}
# sorted_map = {}
# with os.scandir(start_path) as files:
#     i = 0
#     for entry in files:
#         if entry.is_file():
#             file_map[i] = entry.name
#             print("File:   ", entry.name)
#         if entry.is_dir():
#             dir_map[i] = entry.name
#             print("Folder: ", entry.name)
#         i += 1
#
# for item in dir_map.items():
#     sorted_map[item[0]] = item[1]
#
#
# for entry in file_map.items():
#     sorted_map[entry[0]] = entry[1]
#
#
# for item in sorted(sorted_map.items()):
#     print(item)