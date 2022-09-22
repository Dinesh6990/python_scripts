# Modules
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from tkinter import *
import os
from PIL import Image,ImageTk,ImageOps
from PIL import ImageFile
from matplotlib.pyplot import text
ImageFile.LOAD_TRUNCATED_IMAGES = True
import fnmatch
import sys
import threading
from tktooltip import ToolTip

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

imgpath = resource_path('image') # Add Image

# Tkinter, Screen Height & Width
parent = tk.Tk()
parent.title('Image converter Tool')
window_height = 400
window_width = 300
screen_width = parent.winfo_screenwidth()
screen_height = parent.winfo_screenheight()
xLeft = (screen_width/2) - (window_width/2)
yTop = (screen_height/2) - (window_height/2)
parent.geometry('%dx%d+%d+%d' %(window_height,window_width,xLeft,yTop))
parent.resizable(0,0)

# Declaration
set_elements = set()
img_list1 = []
img_list = []
src = ''
dst = ''
notepad_file = StringVar()
src_dir = StringVar()
dst_dir = StringVar()
percent_value = StringVar()
percent_text = StringVar()

def progressbar(val1,val2):
    """Progress Bar & Progress Info"""
    import time
    count_value = val2
    progress_bar['value'] = val1
    percent_value.set(str(round(val1))+'%')
    percent_text.set(str(count_value)+' / '+str(totalcount)+' Images Copied')
    parent.update_idletasks()
    # time.sleep(0.01)

def copy_img(src,dst):
    """Copy only images which are avaliable in list."""
    global totalcount
    img_count = 1
    set_elements=set(img_list)
    img_list1=list((set_elements))
    img_list2 = []
    ivalue= 0
    totalcount = len(img_list1)
    total = (100/len(img_list1))
    for subdirs, dirs, files in os.walk(src):
        for extension in ('*.jpg', '*.jpeg'):
            for file in (fnmatch.filter(files, extension)):
                if file.split('.')[0] in img_list1:
                    f=file.split('.')[0]
                    if f in img_list2:
                        img_list2.remove(f)
                    else:
                        try:
                            i = Image.open(os.path.join(subdirs,file))
                            i = ImageOps.exif_transpose(i)
                            i.thumbnail((1000,1000), Image.ANTIALIAS)
                            rgb_img = i.convert('RGB')
                            rgb_img.save(os.path.join(dst,f+'.JPEG'))
                            ivalue = (ivalue + total)
                            progressbar(ivalue,img_count)
                            img_count+=1
                        except:
                            ivalue = (ivalue + total)
                            progressbar(ivalue,img_count)
                            img_count+=1
                    img_list2.append(file.split('.')[0])                   
    messagebox.showinfo("information", "Task Completed")

def image_count(src):
    """To get the list of images avaliable in Root Directory"""
    for subdirs,dirs, files in os.walk(src):
        for extension in ('*.jpg','*.jpeg'):
            for file in (fnmatch.filter(files, extension)):
                img_list.append(file.split('.')[0])
    return img_list

def open_srcdir():
    """To Display Source Directory Location."""
    src_dir.set('')
    dir1 = askdirectory()
    src_dir.set(dir1)
    return src_dir

def open_dstdir():
    """To Display Destination Directory Location."""
    dst_dir.set('')
    dir1 = askdirectory()
    dst_dir.set(dir1)
    return dst_dir

def clear_contents():
    """Clear all the contents of User Entry"""
    try:
        src_dir.set('')
        dst_dir.set('')
        percent_value.set('')
        percent_text.set('')
        progress_bar.destroy()
    except:
        print('Details Not Updated')
    return src_dir,dst_dir,percent_value,percent_text

def display():
    """To Get Source directory, Destination Directory & Call copy_img function."""
    global progress_bar
    src = src_dir.get()
    dst = dst_dir.get()
    if os.path.exists(src):
        image_count(src)
        if os.path.exists(dst):
        # Progress bar
            progress_bar = ttk.Progressbar(parent,orient='horizontal', length=300, mode='determinate')
            progress_bar.pack()
            progress_bar.place(x=50, y=170)
            percentlabel1 = ttk.Label(parent,textvariable=percent_value)
            percentlabel1.pack()
            percentlabel1.place(x=190, y=170)
            percentlabel2 = ttk.Label(parent,textvariable=percent_text)
            percentlabel2.pack()
            percentlabel2.place(x=150, y=200)
            parent.wm_attributes('-transparentcolor', 'grey')
            x = threading.Thread(target=copy_img, args=(src,dst))
            x.start()
        else:
            messagebox.showinfo("information", "Destination Information Missing or Invalid Path")
            print('Destination Not Selected')
    else:
        messagebox.showinfo("information", "Source Information Missing or Invalid Path")
        print('Source Not Selected')
    return src,dst

# Styling 
style = ttk.Style()
style.configure(
    'BW.TLabel',
    font="Helvetica",
    fontsize=20
)

# Logo Image & Header Info
load= Image.open(imgpath)
render = ImageTk.PhotoImage(load)
img = Label(parent, image=render)
img.place(x=8, y=8)
headerinfo = ttk.Label(parent,text='Convert Images',style='BW.TLabel')
headerinfo.pack()
headerinfo.place(x=160, y=15)

# Labels & Buttons
sourcelocation = tk.Label(parent, text='Source')
sourcelocation.pack()
sourcelocation.place(x=30, y=90)
destinationlocation = tk.Label(parent, text='Destination')
destinationlocation.pack()
destinationlocation.place(x=30, y=130)
submitbtn = tk.Button(parent, text='Submit',width=8,height=1,command=lambda:display())
submitbtn.pack()
submitbtn.place(x=50,y=240)
closebtn = tk.Button(parent, text='Close',width=8,height=1,command=parent.destroy)
closebtn.pack()
closebtn.place(x=160,y=240)
clearbtn = tk.Button(parent, text='Clear',width=8,height=1,command=lambda:clear_contents())
clearbtn.pack()
clearbtn.place(x=270,y=240)

# Browse Files
source_entry = tk.Button(parent, text='...',width=2,height=1 ,command=lambda:open_srcdir())
source_entry.pack()
source_entry.place(x = 340, y = 90)
ToolTip(source_entry, msg='Source Location')
destination_entry = tk.Button(parent, text='...',width=2,height=1, command=lambda:open_dstdir())
destination_entry.pack()
destination_entry.place(x = 340, y = 130)
ToolTip(destination_entry, msg='Destination Location')

# Textbox
sourcelocation_textlabel = tk.Entry(parent, textvariable=src_dir,width=38)
sourcelocation_textlabel.pack()
sourcelocation_textlabel.place(x=105, y=90,height=25)
destinationlocation_textlabel = tk.Entry(parent, textvariable=dst_dir,width=38)
destinationlocation_textlabel.pack()
destinationlocation_textlabel.place(x=105, y=130,height=25)

parent.mainloop()

# To built tkinter .exe file
# pyinstaller --noconfirm --onefile --windowed --add-data 'image.png;.' .\convert_images_tkinter.py
# add your logo ## imgpath = resource_path('image') # line 26