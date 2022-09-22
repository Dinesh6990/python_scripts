import os
import fnmatch
from tkinter import filedialog

directory = filedialog.askdirectory()
os.chdir(directory)
name ='lastimg.jpeg'
pattern = '*.jpeg'

for subdirs, dirs, files in os.walk(directory):
    num_files = len([f for f in os.listdir(subdirs)if f.endswith('.jpeg') and os.path.isfile(os.path.join(subdirs, f))])
    for index,file in enumerate(fnmatch.filter(files, pattern)):
        if index+1==num_files:
            os.rename(os.path.join(subdirs,file), os.path.join(subdirs,name))
            continue