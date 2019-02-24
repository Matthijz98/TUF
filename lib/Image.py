#######################
#       Made By       #
# Gido Scherpenhuizen #
#      S1108069       #
#######################
##
#MERGED BLYAT
# Import libraries used for time conversion and easy path joins
import datetime
from os.path import join as pjoin
import hashlib
import sys

# import libraries used to open an E01 and RAW image file
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


# Function to add data to the database
def addtodb(db, partition_id, partition_offset, parent_key,  md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath, size, extension, f_type):
    db.set_file(partition_id, partition_offset, parent_key,  md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath, size, extension, f_type)


# imagelocation = pjoin("ImageUSBSjors.dd.001")


# Function to retreive data from a directory
def getdirectorydata(db, image, change_dir, parent_key, imagetype):
    for f in main.main(image, imagetype, change_dir):
        if f[10] == "DIR":
            changedir = change_dir
            if f[4] != "." and f[4] != "..":
                addtodb(db, f[0], parent_key, f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11])
                changedir = change_dir + "/" + f[4]
                p_key = f[4]
                getdirectorydata(db, image, changedir, p_key, imagetype)
        else:
            addtodb(db, f[0], parent_key, f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11])


# Function where the file and folder extraction starts
def start(db, image, imagetype):
    for f in main.main(image, imagetype):
        if f[10] == "DIR":
            if f[4] != "." and f[4] != "..":
                addtodb(db, f[0], "", f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11])
                change_dir = f[4]
                parent_key = f[4]
                getdirectorydata(db, image, change_dir, parent_key, imagetype)
        else:
            addtodb(db, f[0], "", f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11])


class main:
    def main(imagefile, imagetype, change_dir=None):
        if imagetype == 'e01':
            image = imagefile.rpartition("/")
            filenames = pyewf.glob(image[2])
            print(filenames)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            # Open Pytsk3 handle on E01 image
            imagehandle = ewf_Img_Info(ewf_handle)
        elif imagetype == 'raw':
            imagehandle = pytsk3.Img_Info(imagefile)
        volume = pytsk3.Volume_Info(imagehandle)

        # Check partitions for partition type and open them
        for partition in volume:
            if partition.len > 2048 and "Unallocated" not in partition.desc.decode('utf-8') and "Extendend" \
                    not in partition.desc.decode('utf-8') and "Primary Table" not in partition.desc.decode('utf-8'):
                try:
                    filesystemObject = pytsk3.FS_Info(imagehandle, offset=partition.start * volume.info.block_size)
                except IOError:
                    _, e, _ = sys.exc_info()
                    print("[-] Unable to open FS:\n {}".format(e))

                partition_id = partition.addr
                partition_offset = partition.start * 512
                # Open directory and change directory
                root_dir = ""
                current_dir = str(change_dir)
                if change_dir is None:
                    open_current_dir = filesystemObject.open_dir(path=root_dir)
                else:
                    open_current_dir = filesystemObject.open_dir(path=current_dir)

                # Make a list where all file data will be stored
                filelist = []

                # Open and check every file for data
                for f in open_current_dir:
                    name = f.info.name.name.decode('utf-8')
                    print(name)
                    if hasattr(f.info.meta, 'type'):
                        if f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                            f_type = "DIR"
                            extension = ""
                        else:
                            f_type = "FILE"
                            if "." in name:
                                extension = name.rsplit(".")[-1].lower()
                            else:
                                extension = ""

                    size = f.info.meta.size
                    f_size = getattr(f.info.meta, "size", 0)
                    if current_dir == "None":
                        filepath = "/" + f.info.name.name.decode('utf-8')
                    else:
                        filepath = "/" + current_dir + "/" + f.info.name.name.decode('utf-8')
                    create = datetime.datetime.fromtimestamp(f.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
                    modify = datetime.datetime.fromtimestamp(f.info.meta.mtime).strftime('%Y-%m-%d %H:%M:%S')

                    if size > 0:
                        hash_obj = hashlib.sha1()
                        hash_obj.update(f.read_random(0, f_size))
                        sha1_hash = hash_obj.hexdigest()

                        hash_obj = hashlib.sha256()
                        hash_obj.update(f.read_random(0, f_size))
                        sha256_hash = hash_obj.hexdigest()

                        hash_obj = hashlib.md5()
                        hash_obj.update(f.read_random(0, f_size))
                        md5_hash = hash_obj.hexdigest()
                    else:
                        sha1_hash = ""
                        sha256_hash = ""
                        md5_hash = ""
                    filelist.append([partition_id, md5_hash, sha256_hash, sha1_hash, name, create, modify, filepath,
                             size, extension, f_type, partition_offset])

                    #if f_type == "FILE" and size > 0:
                    #    with open(pjoin(r"C:\Users\Gido Scherpenhuizen\Documents\OUTPUT", name), "wb") as outfile:
                    #        outfile.write(f.read_random(0, f.info.meta.size))

                # Return the list of file data
                return filelist

    def extract_file(image, filepath, imagetype, name, savelocation, partition_offset):
        if imagetype == 'e01':
            filenames = pyewf.glob(image)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            # Open Pytsk3 handle on E01 image
            imagehandle = ewf_Img_Info(ewf_handle)
        elif imagetype == 'raw':
            imagehandle = pytsk3.Img_Info(image)
        file_system_object = pytsk3.FS_Info(imagehandle, partition_offset)
        file_object = file_system_object.open(filepath)
        output_filepath = pjoin(savelocation, name)
        outfile = open(output_filepath, 'wb')
        filedata = file_object.read_random(0, file_object.info.meta.size)
        outfile.write(filedata)

        def returnpath():
            return output_filepath
