import os
import zipfile
import datetime

import pyewf
import sys
import pytsk3


# Unzip an image to mount/open it
def unzip():
    with zipfile.ZipFile(r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\micro-sd-drone.001", "r") as zip_ref:
        zip_ref.extractall(r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\TEST")


# Mount .ISO file with PowerShell commanf
def importISO():
    os.system(r'PowerShell Mount-DiskImage C:\AD_FTK_6.4.0.iso')


def e01():
    # Declare path to image
    imagefile = r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\TEST\micro-sd-drone.001"

    # Store a python tsk object in a variable
    imagehandle = pytsk3.Img_Info(imagefile)

    # Get and print PartitionTable from image
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print(partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len)

    # Tell libstk where the filesystem is
    filesystemObject = pytsk3.FS_Info(imagehandle, offset=23552)

    # Pick a file
    fileObject = filesystemObject.open("/PHOTO/PICT0000.jpg")

    print("File Inode:", fileObject.info.meta.addr)
    print("File Name", fileObject.info.name.name)
    print("File Creation Time", datetime.datetime.fromtimestamp(fileObject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'))

    # Output file
    outfile = open('DFIRWizard-output', 'wb')
    filedata = fileObject.read_random(0, fileObject.info.meta.size)
    outfile.write(filedata)

def main():
    e01()

if __name__ == "__main__":
    main()
