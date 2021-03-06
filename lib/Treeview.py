import lib.PySimpleGUI as Sg
import lib.Image
import lib.Sqlite
##


#treeview = Sg.Tree(data=tree,
#                   headings=['partition_id', 'file_path', 'size', 'extension', 'file_type'],
#                   def_col_width=50,
#                   right_click_menu=['&Right', ['Extract', 'Upload to VirusTotal']])

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZ\
gJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8\
Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZ\
N5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICs\
Q8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5\
TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='

file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'


# Set the database
#db = lib.Sqlite.Sqlite(path=r"D:\School\2e Jaar\IPFJURI\Images", filename="test")
#db.setup_database()

# Start the image extraction proces


# Add the data of every file and folder to the treeview

def showfiles(db, image, imagetype):
    data = Sg.TreeData()
    lib.Image.start(db, image, imagetype)

    # main
    database = db.get_files()

    for f in database:
        if f[13] == "DIR":
            list = [f[2], f[10], f[11], f[12], f[13]]
            if f[1] == "":
                data.Insert(f[1], f[0], f[7], list, icon=folder_icon)
            else:
                p_key = db.get_parent_key(f[1])
                data.Insert(p_key[0], f[0], f[7], list, icon=folder_icon)

        else:
            list = [f[2], f[10], f[11], f[12], f[13]]
            if f[1] == "":
                data.Insert(f[1], f[0], f[7], list, icon=file_icon)
            else:
                p_key = db.get_parent_key(f[1])
                data.Insert(p_key[0], f[0], f[7], list, icon=file_icon)

    return data

"""
# Create a layout which is used for a window
layout = [[Sg.Text('Welcome to Turtle Forensics!')],
          [treeview]]


win1 = Sg.Window('TUF - Turtle Forensics').Layout(layout)

win4_active = win3_active = win2_active = False

# Turn on the window
while True:
    ev1, vals1 = win1.Read()
    if ev1 == 'Properties':
        win2_active = True

    if vals1[0] == 'selected':
        print("CLICKED")

win1.Close()
"""
