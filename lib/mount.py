from os.path import join as pjoin
import os
import zipfile
import datetime
import argparse

import pyewf
import sys
import pytsk3
from tabulate import tabulate


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


def raw(imagehandle):


    # Get and print PartitionTable from image
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512), partition.len)

    # Tell libstk where the filesystem is
    filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512))

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


# Function used for an e01 imagefile
def e01(filenames):
    ewf_handle = pyewf.handle()
    ewf_handle.open(filenames)
    imagehandle = ewf_Img_Info(ewf_handle)

    # Get and print PartitionTable from image
    partitionTable = pytsk3.Volume_Info(imagehandle)
    for partition in partitionTable:
        print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512),
              partition.len)
        try:
            filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start * 512))
        except:
            print("Partition has no supported file system")
            continue
        print("File System Type Dectected ", filesystemObject.info.ftype)

    for partition in partitionTable:
        if 'NTFS' in partition.desc.decode('utf-8'):
            # Tell libstk where the filesystem is
            filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition.start * 512)

            change_dir = ""     # Variable return from gui
            current_dir = filesystemObject.open_dir(path="/" + change_dir)

            # Only for test purpose
            table = [["Name", "Type", "Size", "Create Date", "Modify Date"]]

            # Functie van maken om aan te roepen vanuit de gui
            for f in current_dir:
                name = f.info.name.name
                if hasattr(f.info.meta, 'type'):
                    if f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                        f_type = "DIR"
                    else:
                        f_type = "FILE"
                    size = f.info.meta.size
                    create = datetime.datetime.fromtimestamp(f.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
                    modify = datetime.datetime.fromtimestamp(f.info.meta.mtime).strftime('%Y-%m-%d %H:%M:%S')
                    table.append([name, f_type, size, create, modify])

            # Only for test purpose
            print(tabulate(table, headers="firstrow"))
"""
            FILE EXPORT !!FUNCTIE VAN MAKEN!!
            
            # Pick a file
            fileObject = filesystemObject.open(pjoin(r'/Windows/System32/winevt/Logs/HardwareEvents.evtx'))
            fileName = str(fileObject.info.name.name.decode('utf-8'))

            # Print info from file
            print("File Inode:", fileObject.info.meta.addr)
            print("File Name", fileName)
            print("File Creation Time", datetime.datetime.fromtimestamp(fileObject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S'))

            # Output file
            completeName = pjoin(, fileName)
            outfile = open(completeName, 'wb')
            filedata = fileObject.read_random(0, fileObject.info.meta.size)
            outfile.write(filedata)"""




def main():
    argparser = argparse.ArgumentParser(description='')

    argparser.add_argument(
        '-i', '--image',
        dest="imagefile",
        action="store",
        type=str,
        default=None,
        required=True,
        help='E01 to extract from'
    )

    argparser.add_argument(
        '-t', '--type',
        dest='imagetype',
        action="store",
        type=str,
        default=False,
        required=True,
        help='Specify image type e01 or raw'
    )

    args = argparser.parse_args()

    if (args.imagetype == "e01"):                               # Vervangen door return uit de GUI
        filenames = pyewf.glob(args.imagefile)

        ewf_handle = pyewf.handle()
        ewf_handle.open(filenames)

        # Open Pytsk3 handle on E01 image
        imagehandle = ewf_Img_Info(ewf_handle)
    else:
        imagehandle = pytsk3.Img_Info(args.imagefile)

    partitionTable = pytsk3.Volume_Info(imagehandle)





    elif (args.imagetype == "raw"):
        print("Raw type")
        imagehandle = pytsk3.Img_Info(url=args.imagefile)
        raw(imagehandle)


if __name__ == "__main__":
    main()
