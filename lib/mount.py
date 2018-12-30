from os.path import join as pjoin
import os
import zipfile
import datetime

import pyewf
import sys
import pytsk3


# Create class to make pytsk3.Img_Info a pyewf function
class ewf_Img_Info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()


# Unzip an image to mount/open it
def unzip():
    with zipfile.ZipFile(r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\micro-sd-drone.001", "r") as zip_ref:
        zip_ref.extractall(r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\TEST")


# Mount .ISO file with PowerShell command
def importISO():
    os.system(r'PowerShell Mount-DiskImage C:\AD_FTK_6.4.0.iso')


def raw():
    # Declare path to image
    imagefile = r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\TEST\micro-sd-drone.001"

    # Store a python tsk object in a variable
    imagehandle = pytsk3.Img_Info(imagefile)

    # Get and print PartitionTable from image
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512), partition.len)

    # Tell libstk where the filesystem is
    filesystemObject = pytsk3.FS_Info(imagehandle, offset=23552)

    # Pick a file
    fileObject = filesystemObject.open("/PHOTO/PICT0000.jpg")
    fileName = str(fileObject.info.name.name.decode('utf-8'))

    # Print info from file
    print("File Inode:", fileObject.info.meta.addr)
    print("File Name", fileName)
    print("File Creation Time", datetime.datetime.fromtimestamp(fileObject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'))

    # Output file
    completeName = pjoin(r"C:\Users\Gido Scherpenhuizen\Documents\,School", fileName)
    outfile = open(completeName, 'wb')
    filedata = fileObject.read_random(0, fileObject.info.meta.size)
    outfile.write(filedata)

def e01():

    filenames = pyewf.glob(r'C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\TEST\Mantooth.E01')
    ewf_handle = pyewf.handle()
    ewf_handle.open(filenames)
    imagehandle = ewf_Img_Info(ewf_handle)

    # Get and print PartitionTable from image
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512),
              partition.len)

    for partition in partitionTable:
        if 'NTFS' in partition.desc.decode('utf'):
            # Tell libstk where the filesystem is
            filesystemObject = pytsk3.FS_Info(imagehandle, offset=32256)

            # Pick a file
            fileObject = filesystemObject.open(r'\Windows\System32\spool\PRINTERS\FP00000.SHD')
            fileName = str(fileObject.info.name.name.decode('utf-8'))

            # Print info from file
            print("File Inode:", fileObject.info.meta.addr)
            print("File Name", fileName)
            print("File Creation Time", datetime.datetime.fromtimestamp(fileObject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'))
"""
    # Output file
    completeName = pjoin(, fileName)
    outfile = open(completeName, 'wb')
    filedata = fileObject.read_random(0, fileObject.info.meta.size)
    outfile.write(filedata)
"""

def main():
    e01()


if __name__ == "__main__":
    main()
