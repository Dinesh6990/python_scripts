import os
import fnmatch
from tkinter import filedialog
from PIL import Image,ImageOps

directory = filedialog.askdirectory()
os.chdir(directory)
output_dir = 'Output Directory'

list_of_files=[]
list_of_index=[]

for subdirs, dirs, files in os.walk(directory):
    for extension in ('*.jpg', '*.jpeg'):
        for index,file in enumerate(fnmatch.filter(files, extension)):           
            if not file.startswith('.'):
                list_of_index.append(index)
                if index==min(list_of_index):
                    ext=file.split('.')[-1]
                    x=subdirs.split('\\')[-1]     
                    name=x
                    list_of_files.append(name)
                    print(os.path.join(output_dir,name))
                    i = Image.open(os.path.join(subdirs,file))
                    i = ImageOps.exif_transpose(i)
                    i.thumbnail((1000,1000), Image.ANTIALIAS)
                    rgb_img = i.convert('RGB')
                    rgb_img.save(os.path.join(output_dir,name+'.JPEG'))
        list_of_index.clear()