import lib.PySimpleGUI as Sg
import lib.Image
import lib.Sqlite
from random import randint

tree = Sg.TreeData()

treegoed = Sg.Tree(data=tree,
                   headings=['partition_id', 'file_md5', 'file_sha256', 'file_sha1', 'title', 'date_created', 'date_last_modified', 'file_path', 'size', 'extension', 'file_type'],
                   auto_size_columns=True,
                   right_click_menu=['&Right', ['Extract', 'Upload to VirusTotal']],
                   enable_events=True)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

"""
def getdirdata(change_dir, parent_key):
    s = 0
    for f in (lib.mount.test.main("micro-sd-drone.001", "raw", change_dir)):
        if f[10] == "DIR":
            if f[4] == "." or f[4] == "..":
                tree.Insert(parent_key, f[4], str(s), f, icon=folder_icon)
                s += 1
                continue
            else:
                tree.Insert(parent_key, f[4], f[4], f, icon=folder_icon)
                change_dir = f[7]
                parent_key = f[4]
                getdirdata(change_dir, parent_key)
        else:
            tree.Insert(parent_key, f[4], f[4], f, icon=file_icon)


for f in (lib.mount.test.main("micro-sd-drone.001", "raw")):
    if f[10] == "DIR":
        if f[4] == "." or f[4] == "..":
            tree.Insert("", f[4], str(q), f, icon=folder_icon)
            q += 1
            continue
        else:
            tree.Insert("", f[4], f[4], f, icon=folder_icon)
            change_dir = f[7]
            parent_key = f[4]
            getdirdata(change_dir, parent_key)
    else:
        tree.Insert("", f[4], f[4], f, icon=file_icon)
"""


def insertfolder(data):
    list = [data[1], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]]
    tree.Insert(data[1], data[0], data[6], list)


def insertfile(data):
    list = [data[1], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]]
    tree.Insert(data[1], data[0], data[6], list, icon=file_icon)


db = lib.Sqlite.Sqlite(path=r"C:\Users\Gido Scherpenhuizen\Documents\,School\IIPFIT5\Project Files", filename="test")
db.setup_database()

lib.Image.start(db)

# main
database = db.get_files()

for f in database:
    if f[12] == "DIR":
        list = [f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11], f[12]]
        if f[1] == "":
            tree.Insert(f[1], f[0], f[6], list, icon=folder_icon)
        else:
            p_key = db.get_parent_key(f[1])
            tree.Insert(p_key[0], f[0], f[6], list, icon=folder_icon)

    else:
        list = [f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11], f[12]]
        if f[1] == "":
            tree.Insert(f[1], f[0], f[6], list, icon=file_icon)
        else:
            p_key = db.get_parent_key(f[1])
            tree.Insert(p_key[0], f[0], f[6], list, icon=file_icon)






"""
def folderinsert(key, display_text, value, p_key=""):
    tree.Insert(p_key, randint(1, 1000000000), display_text, value, icon=folder_icon)


def fileinsert(key, display_text, value, p_key=""):
    tree.Insert(p_key, randint(1, 1000000000), display_text, value, icon=file_icon)


def getdirectorydata(change_dir, parent_key):
    for f in lib.Image.test.main("ImageUSBSjors.dd.001", "raw", change_dir):
        if f[10] == "DIR":
            changedir = change_dir
            if f[4] == "." or f[4] == "..":
                continue
            else:
                tree.Insert(parent_key, f[4], f[4], f, icon=folder_icon)
                changedir = change_dir + "/" + f[4]
                p_key = f[4]
                getdirectorydata(changedir, p_key)
        else:
            tree.Insert(parent_key, f[4], f[4], f, icon=file_icon)


# MAIN
for f in lib.Image.test.main("ImageUSBSjors.dd.001", "raw"):
    if f[10] == "DIR":
        if f[4] != "." and f[4] != "..":
            folderinsert(f[4], f[4], f)
            change_dir = f[4]
            parent_key = f[4]
            getdirectorydata(change_dir, parent_key)
        # else:
            # folderinsert(f[4], f[4], randint(0, 100000), f)
    else:
        fileinsert(f[4], f[4], f, "")
"""

layout = [[Sg.Text('Welcome to Turtle Forensics!')],
          [treegoed]]


win1 = Sg.Window('TUF - Turtle Forensics').Layout(layout)

win4_active = win3_active = win2_active = False

while True:
    ev1, vals1 = win1.Read()
    if ev1 == 'Properties':
        win2_active = True

    if ev1 == 'selected':
        print("CLICKED")

win1.Close()
