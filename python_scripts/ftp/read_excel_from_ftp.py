from ftplib import FTP
import os
import datetime
import warnings
import os.path
from cryptography.utils import CryptographyDeprecationWarning
import pandas as pd

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko

class InventoryView:
    # FTP Server credentials
    ftp_ip = 'ftp ip address'
    ftp_userid = 'username'
    ftp_password = 'password'
    ftp_direc = 'ftp dir'
    
    # Local 
    local_direc = 'local directory'


    # Linux Server
    hostname = 'ip address'
    prod_username = 'username'
    prod_password = 'password'
    prod_direc = 'folder1'
    prod_direc_done = 'folder2'

    def __init__(self,filename):
        self.filename = filename

    def ftp_download(self):
        """To Get the Excel file from FTP Server"""
        ftp = FTP()
        ftp.connect(InventoryView.ftp_ip)
        ftp.login(InventoryView.ftp_userid,InventoryView.ftp_password)
        ftp.cwd(InventoryView.ftp_direc)
        d_location = os.path.join(InventoryView.local_direc, self.filename)
        
        with open(d_location,'wb') as file:
            ftp.retrbinary(f'RETR {self.filename}', file.write)
        ftp.quit()
        print('downloaded')
        
    def modify(self):
        """Load the data to DataFrame and write to different csv files sheet wise"""
        os.chdir(InventoryView.local_direc)
        df_sheets = pd.ExcelFile(self.filename)
        list_xls = []
        for sheet in df_sheets.sheet_names:
            list_xls.append(sheet)
            
        for xl in list_xls:
            df = pd.read_excel(self.filename,sheet_name=xl)
            name=xl+'_'+datetime.datetime.now().strftime('%Y%m%d')+'.csv'
            df = df.dropna(subset=['column_name'])
            df.to_csv(name.lower(),index=False)

    def file_transfer(self):
        """Transfer list of files from local directory to Linux server"""
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=InventoryView.hostname, username=InventoryView.prod_username, password=InventoryView.prod_password)
        sftp_client = ssh_client.open_sftp()
        
        os.chdir(InventoryView.local_direc)

        file_list = []
        try:
            for i,j,k in os.walk(InventoryView.local_direc):
                for file in k:
                    file_list.append(file)
        finally:
            file_list.remove(self.filename)

        folder_list =  [InventoryView.prod_direc,InventoryView.prod_direc_done]
        try:
            for folder in folder_list:
                print(folder)
                for files in file_list:
                    if os.path.exists(files) and folder ==InventoryView.prod_direc:
                        sftp_client.put(files,folder+files[:-13]+'.csv')
                    elif os.path.exists(files) and folder == InventoryView.prod_direc_done:
                        sftp_client.put(files,folder+files)
                    else:
                        print('File Not Found in your local directory')
        finally:
            sftp_client.close()
            ssh_client.close()
            print('Success')

    def delete_files(self):
        """Delete all the files in the directory"""
        for i,j,k in os.walk(InventoryView.local_direc):
            for file in k:
                os.remove(file)    

# Define file name
s = datetime.datetime.now().strftime('%d-%m-%Y')
s_date = datetime.datetime.strptime(s,'%d-%m-%Y')
x =(s_date-datetime.timedelta(days=2)).date()
filename = x.strftime('%d-%m-%Y')+'_filename.xlsx'

# Class object and Function call
a = InventoryView(filename)
a.ftp_download()
a.modify()
a.file_transfer()
a.delete_files()