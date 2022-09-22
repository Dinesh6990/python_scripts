import os
import pandas as pd
import datetime
import fnmatch
from tkinter import filedialog
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%I_%M_%p') 
filename='output'+time_now+'.xlsx'

directory = filedialog.askdirectory()
os.chdir(directory)

path = directory
files = os.listdir(path)

files_xls = []
for subdirs, dirs, files in os.walk(directory):
    for extension in ('*.xlsx'):
        for index,f in enumerate(fnmatch.filter(files,extension)):
            if not f.startswith('~'):
                if f.split('.')[-1]=='xlsx':
                    files_xls.append(f)


df = pd.DataFrame()
        
for f in files_xls:
    data = pd.DataFrame()
    data = pd.read_excel(f, 'sheet name',skiprows=3)
    data  = data.iloc[:,13:]
    data = data.dropna(subset=['column']) # Remove null values
    data.append(data)
    df = pd.concat([data,df])
    
df.dropna(how='all',inplace=True)
df.to_excel(filename, index=False)