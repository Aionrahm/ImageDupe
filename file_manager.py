import tkinter as tk
from tkinter import filedialog
import glob
import hashlib
import os
import time


class File:
    file_list = {}
    count = 0
    time = 0
    file_num = 0

    def start(self):

        folder = self.get_folder()
        self.time = time.time()
        self.get_files(folder)
        self.delete_dupes()
        self.print_count()

    @staticmethod
    def get_folder():
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        return folder

    def get_files(self, folder):
        files = [log for log in glob.glob(folder + '/*') if not os.path.isdir(log)]
        self.file_num = len(files)
        for item in files:
            with open(item, 'rb') as file_name:
                data = file_name.read()
                md5_returned = hashlib.md5(data).hexdigest()
            self.file_list.setdefault(md5_returned, [])
            self.file_list[md5_returned].append(item)

    def delete_dupes(self):
        for key in self.file_list.keys():
            if len(self.file_list[key]) > 1:
                for item in self.file_list[key][:-1]:
                    os.remove(item)
                    self.count += 1

    def print_count(self):
        print("Out of {} files you removed {} dupes for {} minutes.".format(self.file_num, self.count, (time.time() - self.time)/60))
