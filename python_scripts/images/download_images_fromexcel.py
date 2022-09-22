import pandas as pd
import openpyxl
from openpyxl_image_loader import SheetImageLoader

#loading the Excel File and the sheet
pxl_doc = openpyxl.load_workbook('filename.xlsx')
sheet = pxl_doc['sheetname']

df = pd.read_excel('filename.xlsx',sheet_name ='sheetname')
x = df['item name'].to_list()

for i,j in enumerate(x):
    #calling the image_loader
    image_loader = SheetImageLoader(sheet)
    image = image_loader.get('A'+str(i+2))
    image.save(x[i]+'.jpg')