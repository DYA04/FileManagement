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
from constants import audio_extensions, image_extensions, video_extensions, document_extensions


class DirectoryManager():
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