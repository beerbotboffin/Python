'''

    Upload web files (html, css, jpg) for site to FTP server
    Shane Frost Jul 2020

    modified
    20200719    Added support to get credentials from keepass.
                Changed so that only modified files are uploaded to save bandwidth
                
'''

from ftplib import FTP
import os
import datetime
from datetime import datetime
from datetime import date
from time import gmtime, strftime
import time
from pykeepass import PyKeePass

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def getPassword(titleName):
    entry = kp.find_entries(title=titleName, first=True)
    return entry.password

# load keepass database
kp = PyKeePass('C:\\Users\\<username>\\Documents\\<keepass file>.kdbx',
               keyfile='C:\\Users\\<username>\\Documents\\<keyfile>.key',
               password='<your password>')


# The keepass group 
group = kp.find_groups(name='Internet', first=True)
# find the entry by its title
entry = kp.find_entries(title='TPG', first=True)

ftp = FTP(entry.url)
ftp.login(entry.username, entry.password)
        
localFilepath = 'N:\\Web\\'
ignoreFile = 'ignore.txt'
fileName = 'default.css'
ignore = []
files = []
folders = []

# Get the files in the source directory
for file in os.listdir(localFilepath):
    lastmodified = os.stat(os.path.join(localFilepath, file)).st_mtime
    if days_between(str(datetime.today())[0:10],str(datetime.fromtimestamp(lastmodified))[0:10]) < 1: 
        if file.find('.') != -1:
            files.append(file)
        else:
            folders.append(file)

# Get the files to ignore
fi = open(localFilepath + ignoreFile,'r')
for x in fi:
    ignore.append(x.strip())


# Upload the files to the server
for x in files:    
    ok = True
    for xx in ignore:
        if x == xx:
            ok = False
    if ok == True:
        print(x)
        ftp.storbinary('STOR ' + x, open(localFilepath + x, 'rb'))

print('*********************************************')

# Upload the images to the server
for x in folders:
    ftp.cwd('/' + x);
    print(x)
    for file in os.listdir(localFilepath + x):
        if file.find('.jpg') > 0:
            lastmodified = os.stat(os.path.join(localFilepath, x , file)).st_mtime
            if days_between(str(datetime.today())[0:10],str(datetime.fromtimestamp(lastmodified))[0:10]) < 1: 
                print(localFilepath + x + '\\' + file)
                ftp.storbinary('STOR ' + file, open(localFilepath + x + '\\' + file, 'rb'))
    
ftp.quit() # Terminate the FTP connection







