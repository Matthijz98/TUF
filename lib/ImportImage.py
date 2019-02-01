#######################
#       Made By       #
# Gido Scherpenhuizen #
#      S1108069       #
#######################

import datetime
import hashlib
from os.path import join as pjoin

import lib.Sqlite

import pyewf
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
            outfile.write(filedata)
"""


# db = lib.Sqlite.Sqlite(path=r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\Project Files", filename="test")
# db.setup_database()


def addtodb(db, partition_id, parent_key, md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath, size,
            extension, f_type):
    db.set_file(partition_id, parent_key, md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath, size,
                extension, f_type)


def getdirectorydata(db, change_dir, parent_key):
    for f in test.main("ImageUSBSjors.dd.001", "raw", change_dir):
        if f[10] == "DIR":
            changedir = change_dir
            if f[4] != "." and f[4] != "..":
                print(f[4])
                addtodb(db, f[0], parent_key, f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10])
                changedir = change_dir + "/" + f[4]
                p_key = f[4]
                getdirectorydata(db, changedir, p_key)
        else:
            addtodb(db, f[0], parent_key, f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10])


def start(db):
    for f in test.main("ImageUSBSjors.dd.001", "raw"):
        if f[10] == "DIR":
            if f[4] != "." and f[4] != "..":
                addtodb(db, f[0], "", f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10])
                change_dir = f[4]
                parent_key = f[4]
                getdirectorydata(db, change_dir, parent_key)
        else:
            addtodb(db, f[0], "", f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10])


class test:
    def main(imagefile, imagetype, change_dir=None):
        if imagetype == 'e01':  # Vervangen door return uit de GUI
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

        """
        for partition in volume:
            print(partition.addr, partition.desc.decode('utf-8'), "%ss(%s)" % (partition.start, partition.start * 512),
                partition.len)
            try:
                filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start * 512))
            except:
                print("Partition has no supported file system")
                continue
            print("File System Type Dectected ", filesystemObject.info.ftype)
        """

        for partition in volume:
            if 'NTFS' in partition.desc.decode('utf-8') or 'FAT16' in partition.desc.decode('utf-8') \
                    or 'FAT32' in partition.desc.decode('utf-8') or 'EXT2' in partition.desc.decode('utf-8') \
                    or 'EXT3' in partition.desc.decode('utf-8') or 'EXT4' in partition.desc.decode('utf-8'):
                partition_id = partition.addr
                filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition.start * 512)

                root_dir = ""
                current_dir = str(change_dir)
                if change_dir is None:
                    open_current_dir = filesystemObject.open_dir(path=root_dir)
                else:
                    open_current_dir = filesystemObject.open_dir(path=current_dir)

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
                    size = f.info.meta.size
                    filepath = pjoin(current_dir, "/", f.info.name.name.decode('utf-8'))
                    create = datetime.datetime.fromtimestamp(f.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
                    modify = datetime.datetime.fromtimestamp(f.info.meta.mtime).strftime('%Y-%m-%d %H:%M:%S')

                    # if f_type == "FILE":
                    # print(pjoin("/", filepath))
                    # fileobject = filesystemObject.open(pjoin(filepath))
                    # completeName = pjoin(filepath)
                    # outfile = open(pjoin('C:/Users/Gido Scherpenhuizen/Documents/,School/OUTPUT/' + f.info.name.name.decode('utf-8')), 'wb')
                    # filedata = fileobject.read_random(0, fileobject.info.meta.size)
                    # outfile.write(filedata)
                    # outfile.close()
                    # f_size = getattr(f.info.meta, "size", 0)
                    # md5_hash = hashlib.md5()  # MD5 FUNCTIE VAN DYLAN
                    # md5_hash.update(filedata)
                    # print(md5_hash.hexdigest)

                    # sha256_hash = hashlib.sha256()
                    # sha256_hash.update(f.read_random(outfile))
                    # sha256_hash.hexdigest

                    # sha1_hash = hashlib.sha1()
                    # sha1_hash.update(f.read_random(outfile))
                    # sha1_hash.hexdigest

                    md5_hash = ""
                    sha256_hash = ""
                    sha1_hash = ""

                    filelist.append([partition_id, md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath,
                                     size, extension, f_type])
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