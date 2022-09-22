# Modules
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter.filedialog import askdirectory, askopenfile
from tkinter import *
from tkinter import font as tkFont
import os
from PIL import Image,ImageTk,ImageOps
from PIL import ImageFile
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

imgpath = resource_path('image.png')


# Tkinter, Screen Height & Width
parent = tk.Tk()
parent.title('Images Copy Tool')
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

def avaliable_imgs(src):
    global img_list2
    img_list2 = []
    for subdirs,dirs, files in os.walk(src):
        for extension in ('*.jpg','*.jpeg'):
            for file in (fnmatch.filter(files, extension)):
                img_list2.append(file.split('.')[0])
    return img_list2

def progressbar(val1,val2):
    import time
    count_value = val2
    progress_bar['value'] = val1
    percent_value.set(str(round(val1))+'%')
    percent_text.set(str(count_value)+' / '+str(totalcount)+' Images Copied')
    parent.update_idletasks()
    time.sleep(0.2)

def copy_img(src,dst):
    """Copy only images which are avaliable in list."""
    global totalcount
    img_count = 1
    set_elements=set(img_list)
    img_list1=list((set_elements))
    img_list3 = []
    for x in img_list1:
        if x in img_list2:
            img_list3.append(x)
    img_list4 = []
    ivalue=0
    totalcount = len(img_list3)
    total = (100/len(img_list3))
    for subdirs, dirs, files in os.walk(src):
        for extension in ('*.jpg', '*.jpeg'):
            for file in (fnmatch.filter(files, extension)):
                if file.split('.')[0] in img_list3:                    
                    f=file.split('.')[0]
                    ext = file.split('.')[-1]
                    if f in img_list4:
                        img_list4.remove(f)
                    else:
                        print(file)
                        try:
                            i = Image.open(os.path.join(subdirs,file))
                            i = ImageOps.exif_transpose(i)
                            i.thumbnail((1000,1000), Image.ANTIALIAS)
                            rgb_img = i.convert('RGB')
                            rgb_img.save(os.path.join(dst,f+'.'+ext))
                            ivalue = (ivalue + total)
                            progressbar(ivalue,img_count)
                            img_count+=1
                        except:
                            ivalue = (ivalue + total)
                            progressbar(ivalue,img_count)
                            img_count+=1
                    img_list4.append(file.split('.')[0])
                    

def open_file():
    """To get the Input list from Notepad."""
    notepad_file.set('')
    try:
        file = askopenfile(mode='r',filetypes=[('Text Files','*.txt')])
        notepad_file.set(file.name)
        if os.path.exists(notepad_file.get()):
            for i in file.readlines():
                img_list.append(i.strip())
        else:
            print(notepad_file.get())
            messagebox.showinfo("information", "Invalid Path")
    except:
        print('Input not provided')
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
        notepad_file.set('')
        src_dir.set('')
        dst_dir.set('')
        percent_value.set('')
        percent_text.set('')
        progress_bar.destroy()
    except:
        print('Details Not Updated')
    return notepad_file,src_dir,dst_dir,percent_value,percent_text

def display():
    """To Get Source directory, Destination Directory & Call copy_img function."""
    global progress_bar
    src = src_dir.get()
    dst = dst_dir.get()
    if os.path.exists(notepad_file.get()):
        if os.path.exists(src):
            avaliable_imgs(src)
            if os.path.exists(dst):
            # Progress bar
                progress_bar = ttk.Progressbar(parent,orient='horizontal', length=300, mode='determinate')
                progress_bar.pack()
                progress_bar.place(x=50, y=180)
                percentlabel1 = ttk.Label(parent,textvariable=percent_value)
                percentlabel1.pack()
                percentlabel1.place(x=190, y=180)
                percentlabel2 = ttk.Label(parent,textvariable=percent_text)
                percentlabel2.pack()
                percentlabel2.place(x=150, y=210)
                x = threading.Thread(target=copy_img, args=(src,dst))
                x.start()
            else:
                messagebox.showinfo("information", "Destination Information Missing or Invalid Path ")
                print('Destination Not Selected')
        else:
            messagebox.showinfo("information", "Source Information Missing or Invalid Path")
            print('Source Not Selected')
    else:
        messagebox.showinfo("information", "Input List Missing or Invalid Path ")
        print('Input List Not Selected')
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
headerinfo = ttk.Label(parent,text='Copy Images',style='BW.TLabel')
headerinfo.pack()
headerinfo.place(x=160, y=15)

# Labels & Buttons
uploadfile = tk.Label(parent,text='Image List')
uploadfile.pack()
uploadfile.place(x=30, y=70)
sourcelocation = tk.Label(parent, text='Source')
sourcelocation.pack()
sourcelocation.place(x=30, y=105)
destinationlocation = tk.Label(parent, text='Destination')
destinationlocation.pack()
destinationlocation.place(x=30, y=140)
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
uploadfile_entry = tk.Button(parent, text='...', command=lambda:open_file())
uploadfile_entry.pack()
uploadfile_entry.place(x = 345, y = 70)
ToolTip(uploadfile_entry, msg='Input List')
source_entry = tk.Button(parent, text='...', command=lambda:open_srcdir())
source_entry.pack()
source_entry.place(x = 345, y = 105)
ToolTip(source_entry, msg='Source Location')
destination_entry = tk.Button(parent, text='...', command=lambda:open_dstdir())
destination_entry.pack()
destination_entry.place(x = 345, y = 140)
ToolTip(destination_entry, msg='Destination Location')

# Textbox
uploadfile_textlabel = tk.Entry(parent, textvariable=notepad_file,width=38)
uploadfile_textlabel.pack()
uploadfile_textlabel.place(x=105, y=70, height=25)
sourcelocation_textlabel = tk.Entry(parent, textvariable=src_dir,width=38)
sourcelocation_textlabel.pack()
sourcelocation_textlabel.place(x=105, y=105, height=25)
destinationlocation_textlabel = tk.Entry(parent, textvariable=dst_dir,width=38)
destinationlocation_textlabel.pack()
destinationlocation_textlabel.place(x=105, y=140, height=25)

parent.mainloop()

# To built tkinter .exe file
# pyinstaller --noconfirm --onefile --windowed --add-data 'image.png;.' .\convert_images_tkinter.py
# add your logo ## imgpath = resource_path('image') # line 26