#!/usr/bin/env python3
import os
import shutil
import sqlite3
import datetime

frmdir = 'G:/Glacier/Files/'
dstdir = 'G:/STORE/'
mapping = 'mapping.sqlite3'


def move(frm, dst, timestamp):
    """ Copy file from source to destinatin """
    exists=[]                          # cache existing dirs
    dir = os.path.normpath(dstdir+dst) # normalize destination	
    dirname = os.path.dirname(dir)	   # fetch dirname of dst
    
    if dirname in exists:
        pass
    else:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        exists.append(dirname)

    print(dir)
    shutil.copyfile(frmdir+frm, dir)
    os.utime(dir, (timestamp, timestamp))


def main(mapping):
    ''' retrieve list of files from the mapping and move files
        to the appropriate location
    '''
    notfound=[]
    found=[]
    conn = sqlite3.connect(mapping)

    c = conn.cursor()
    c.execute('select shareName || "/" || basePath, archiveID, lastBkpTime from file_info_tb')

    row = c.fetchone()
    while not row is None:
        if not os.path.isfile(frmdir+row[1]):
            notfound.append(row[1])
        else:
            found.append(row[1])
            move(row[1], row[0], row[2])
        row = c.fetchone()

    return found,notfound


if __name__ == "__main__":
    found,notfound = main(frmdir+'/mapping.sqlite3')
    print(f"{len(found)} files found and {len(notfound)} not found")
