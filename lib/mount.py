from os.path import join as pjoin
from pathlib import Path
import os
import zipfile
import datetime
import argparse
import hashlib

import lib.Sqlite

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

class test():
    def main(imagefile, imagetype, change_dir=""):
        if (imagetype == "e01"):  # Vervangen door return uit de GUI
            filenames = pyewf.glob(imagefile)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            # Open Pytsk3 handle on E01 image
            imagehandle = ewf_Img_Info(ewf_handle)
        else:
            imagehandle = pytsk3.Img_Info(imagefile)
        volume = pytsk3.Volume_Info(imagehandle)
        # test.printpartitiontable(imagehandle, volume)
        # test.listfiles(volume, imagehandle)

        #for partition in volume:
         #   print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512),
          #        partition.len)
           # try:
            #    filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start * 512))
            #except:
                # print("Partition has no supported file system")
             #   continue
            # print("File System Type Dectected ", filesystemObject.info.ftype)

        for partition in volume:
            # Variabele return vanuit de GUI met gekozen partitie
            if 'FAT16' in partition.desc.decode('utf-8'):
                partition_id = partition.addr
                filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition.start * 512)

                root_dir = "/"
                change_dir = change_dir + "/"   # Variable return from gui
                current_dir = root_dir + change_dir
                open_current_dir = filesystemObject.open_dir(path=current_dir)

                # Only for test purpose
                table = [["Name", "Type", "Size", "Create Date", "Modify Date"]]

                # Functie van maken om aan te roepen vanuit de gui
                filelist = []
                for f in open_current_dir:
                    name = f.info.name.name.decode('utf-8')
                    if hasattr(f.info.meta, 'type'):
                        if f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                            f_type = "DIR"
                            extension = ""
                        else:
                            f_type = "FILE"
                            if "." in name:
                                extension = name.rsplit(".")[-1].lower()
                    """
                    md5_hash = hashlib.md5()  # MD5 FUNCTIE VAN DYLAN
                    md5_hash.update(f.read_random(0, f_size))
                    md5_hash2 = md5_hash.hexdigest

                    sha256_hash = hashlib.sha256()
                    sha256_hash.update(f.read_random(0, f_size))
                    sha256_hash2 = sha256_hash.hexdigest

                    sha1_hash = hashlib.sha1()
                    sha1_hash.update(f.read_random(0, f_size))
                    sha1_hash2 = sha1_hash.hexdigest
                    """
                    md5_hash2 = ""
                    sha256_hash2 = ""
                    sha1_hash2 = ""


                    size = f.info.meta.size
                    filepath = current_dir + f.info.name.name.decode('utf-8')
                    create = datetime.datetime.fromtimestamp(f.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
                    modify = datetime.datetime.fromtimestamp(f.info.meta.mtime).strftime('%Y-%m-%d %H:%M:%S')
                    filelist.append([partition_id, md5_hash2, sha256_hash2, sha1_hash2, name, create, modify, filepath, size, extension, f_type])
                # db = lib.Sqlite.Sqlite(path=r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\Project Files", filename="test")
                # db.setup_database()
                # db.set_files(filelist)
                return filelist

"""
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

if __name__ == "__main__":
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

    test.main(args.imagefile, args.imagetype)
