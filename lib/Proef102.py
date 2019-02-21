import lib.PySimpleGUI as Sg
import lib.Image
import lib.Sqlite

tree = Sg.TreeData()

treegoed = Sg.Tree(data=tree,
                   headings=['partition_id', 'file_path', 'size', 'extension', 'file_type'],
                   def_col_width=50,
                   right_click_menu=['&Right', ['Extract', 'Upload to VirusTotal']],
                   pad=20)

extract_button = Sg.Button(button_text="Extract")
hash_button = Sg.Button(button_text="Hash file")

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZ\
gJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8\
Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZ\
N5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICs\
Q8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5\
TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='

file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6X\
G54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVT\
A1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDk\
xGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsN\
kAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'


# Set the database
db = lib.Sqlite.Sqlite(path=r"C:\Users\Gido Scherpenhuizen\Documents", filename="test")
db.setup_database()

# Start the image extraction proces
lib.Image.start(db)

# main
database = db.get_files()

# Add the data of every file and folder to the treeview
for f in database:
    if f[12] == "DIR":
        list = [f[2], f[9], f[10], f[11], f[12]]
        if f[1] == "":
            tree.Insert(f[1], f[0], f[6], list, icon=folder_icon)
        else:
            p_key = db.get_parent_key(f[1])
            tree.Insert(p_key[0], f[0], f[6], list, icon=folder_icon)

    else:
        list = [f[2], f[9], f[10], f[11], f[12]]
        if f[1] == "":
            tree.Insert(f[1], f[0], f[6], list, icon=file_icon)
        else:
            p_key = db.get_parent_key(f[1])
            tree.Insert(p_key[0], f[0], f[6], list, icon=file_icon)


# Create a layout which is used for a window
layout = [[Sg.Text('Welcome to Turtle Forensics!')],
          [treegoed],
          [hash_button],
          [extract_button]]


win1 = Sg.Window('TUF - Turtle Forensics').Layout(layout)

win4_active = win3_active = win2_active = False

# Turn on the window
while True:
    ev1, vals1 = win1.Read()
    if ev1 == 'EXTRACT BLYAT':
        print("BLYAT EXTRACTED")
        for filelist in vals1:
            for file in filelist:
                print(db.get_file_path(file))

    if ev1 == "Extract":
        for file_id in vals1[0]:
            filepath_list = db.get_file_path(file_id)
            print(filepath_list)
            for filepath_from_filepath_list in filepath_list[0]:
                file_name_list = db.get_file_name(file_id)
                for file_name in file_name_list[0]:
                    lib.Image.test.extract_file("ImageUSBSjors.dd.001", filepath_from_filepath_list, "raw", file_name, r"C:\Users\Gido Scherpenhuizen\Documents\OUTPUT")

    if ev1 == "Hash file":
        for file_id in vals1[0]:
            hash_list = db.get_file_hash(file_id)
            hash_tuple = hash_list[0]
            text = "md5: " + hash_tuple[0] + "\n \n" + "sha256: " + hash_tuple[1] + "\n \n" + "sha1: " + hash_tuple[2]
            Sg.Popup("File Hash", text)




win1.Close()
