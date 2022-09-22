import pandas as pd
import warnings
import os
from tkinter import filedialog

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

path = filedialog.askopenfilename()
filename = path.split('/')[-1]
d = path.split('/')[:-1:]
direc = '/'.join(d)
os.chdir(direc)
outputfile = 'output.xlsx'

df = pd.read_csv(filename)
repeatcolumn = df.columns[-1]
df_new = df.loc[df.index.repeat(df[repeatcolumn])]
df_new[repeatcolumn] = df_new[repeatcolumn]=1

df_new.to_excel(outputfile, index=False)