#######################
# Main/GUI            #
# Oskar Brynkus       #
# s1105798            #
#######################
##
# All the libraries that are being imported.
# config parser to save settings in a config file
import configparser
# Import OS: allows the use of using the same path on multiple systems
import os
# Import PySimpleGUI: enables the use of the pysimplegui
import PySimpleGUI as Sg
# Imports the script Sqlite from the directory 'lib' into the main.py script which enables the use of a sqlite database
from lib import Sqlite
# Imports the script VirusTotal from the directory 'lib' into the main.py script which enables the use of virustotal
from lib import VirusTotal
# Imports the script Wireshark from the directory 'lib' into the main.py script which enables the use of wireshark
from lib.Wireshark import Wireshark
# Imports the script Treeview from the directory 'lib' into the main.py script which enables the use of the treeview
from lib import Treeview

from lib import Image


virustotal_api = ""
# make a config object
config = configparser.ConfigParser()
# open config
config.read('config.ini')
# check if the option is set in the config file
if config.has_option("Virus total", "api key") is True:
    # if there is a option load it from the file and use it
    virustotal_api = config['Virus total']['api key']
# the path where to programm is located
path = os.path.dirname(os.path.realpath(__file__))
name = 'database'
db = ''
# set the login state to False
loggedin = False
# the currently open case
active_case = ''

# a method that makes a case
def makeCase(number, title, note):
    values = {"number": number, "title": title, "note": note}
    db.set_case(values)


# The layout of the window is created with the 'layout' variable
layout = [[Sg.Text('At which location would you like to save the TUF database?')],
          [Sg.Input(path), Sg.FolderBrowse()],
          [Sg.T(' ' * 25), Sg.Button('Yes'), Sg.Button('No')]]
# Giving the window the variable layout
startWindow = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout)

# When all windows are false then startWindow is active
treeviewWindow_active = loggingWindow_active = createCaseWindow2_active = createCaseWindow_active = win4_active = \
    loggedWindow_active = loginWindow_active = False

# When event and values are startWindow then they show that window.
while True:
    ev1, vals1 = startWindow.Read()
    # If the 'close' button is pushed the program is going to stop with running
    if ev1 is None:
        break
    # If the 'No' button is pushed the program is going to stop with running
    if ev1 == 'No':
        break
    # If the 'Yes' button is pushed the program is going to save the database in the location you've chose
    if ev1 == 'Yes':
        if path != vals1[0]:
            path = vals1[0]
        db = Sqlite.Sqlite(path, name)
        exists = os.path.isfile(path + '/' + name + ".db")
        if not exists:
            # Store configuration file values
            db.setup_database()
    # If the 'Yes' button is pushed the program is going to activate the 2nd window and hide the previous window.
    if not loginWindow_active and ev1 == 'Yes':
        loginWindow_active = True
        startWindow.Hide()
        # The layout of the window is created with the 'layout' variable
        layout2 = [[Sg. Text('Login as a TUF user or create a new user account.')],
                   [Sg.Text('Username'), Sg.Input()],
                   [Sg.Text('Password'), Sg.Input(password_char='*')],
                   [Sg.Button('Login'), Sg.Button('Create User')]]
        # Giving the window the variable layout
        loginWindow = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout2)

    # if loginWindow is active then the code underneath will run
    if loginWindow_active:
        ev2, vals2 = loginWindow.Read()
        username = vals2[0]
        password = vals2[1]
        # while the user hasn't logged in then the program will keep showing the same window
        while loggedin is False:
            if ev2 == 'Login':
                # giving variables values which will check if they match in the database
                check_loggedin = db.check_user(username, password)
                # if the username and password are the same as the ones in the database then a popup will show up
                if check_loggedin is True:
                    loggedin = True
                    Sg.Popup("You've been logged in successfully! Welcome " + vals2[0] + "!")
                    break
                # if the values don't correspond with the values in the database then a popup will show up
                elif check_loggedin is False or username == "":
                    loggedin = False
                    Sg.Popup("This combination of username and password does not exist.")
                    ev2, vals2 = loginWindow.Read()
                # if the upper 2 IF statement aren't used then it will show a popup
                else:
                    Sg.Popup("Something went wrong. Try again.")
                    loggedin = False
            # if the user tries to create a new account with a username that already exists it will show a popup screen
            # and keep repeating the same window until he creates a new user or logs in
            if ev2 == 'Create User' and loggedin is False:
                created = db.check_username(vals2[0])
                username = vals2[0]
                password = vals2[1]

                if username == "" or password == "":
                    Sg.Popup("The username or password field can not be empty")
                    ev2, vals2 = loginWindow.Read()

                elif created is False:
                    db.set_user(username=vals2[0], password=vals2[1])
                    Sg.Popup("The user with the name " + vals2[0] + " has been created!")
                    loggedin = True

                else:
                    Sg.Popup("This user already exists!")
                    ev2, vals2 = loginWindow.Read()

            if ev2 is None:
                break
    # if loggedWindow and loggedin is True then the code underneath will run
    if not loggedWindow_active and loggedin is True:
        cases = db.get_cases()
        table = Sg.Table(cases,
                         headings=["case", "case id", "title", "description", "date created"],
                         enable_events=True)
        loggedWindow_active = True
        # hides the window loginWindow
        loginWindow.Hide()
        # The layout of the window is created with the 'layout' variable
        layout3 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                   [Sg.Text('', key='OUTPUT')],
                   [Sg.Text('Would you like to create a new case or open a recent one?')],
                   [table],
                   [Sg.Button('Open Case'), Sg.Button('Create Case'), Sg.Button('VirusTotal'), Sg.Button('Logging'), Sg.Button('Treeview')]]
        # Giving the window the variable layout
        loggedWindow = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout3)

        while True:
            if loggedWindow_active:
                ev3, vals3 = loggedWindow.Read()
                # if the user pressed the button virustotal then it will execute the code beneath it
                if ev3 == 'VirusTotal':
                    # check if api key is set
                    if virustotal_api == "":
                        # if not set ask the user
                        virustotal_api = Sg.PopupGetText('Please provide a VirusTotal API key', 'VirusTotal api')
                        # set the config option to the input given by the user
                        config.add_section("Virus total")
                        config['Virus total']['api key'] = virustotal_api
                        db.log_item(title="Virus total API key opgeslagen", details="API key: " + virustotal_api)
                        # write the config file to config.ini
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                    vt = VirusTotal.VirusTotal(virustotal_api)
                    # the chosen file will get send to virustotal
                    #testfile = Sg.PopupGetFile('Which file would you like to check?', 'TUF - VirusTotal')
                    # functie test_file uitvoeren
                    # hier wordt de functie aangeroepen uit de klasse met de constructor
                    #virustotal = vt.test_file(testfile)



                if ev3 == 'Open Case':
                    active_case = cases[vals3[0][0]][0]
                    break

                if ev3 == 'Treeview':
                    treeviewWindow_active = True
                    loggedWindow_active = False
                    loggedWindow.Hide()
                    image = Sg.PopupGetFile('Which image would you like to open?', 'TUF - Choose image')

                    treeview = Sg.Tree(data=Treeview.showfiles(db, image),
                                       headings=['partition_id', 'file_path', 'size', 'extension', 'file_type'],
                                       def_col_width=50,
                                       right_click_menu=['&Right', ['Extract', 'Upload to VirusTotal']])

                    layout7 = [[Sg.Text('Welcome to Turtle Forensics!')],
                               [treeview]]

                    treeviewWindow = Sg.Window('TUF - Treeview', icon='ICON.ico').Layout(layout7)

                    if treeviewWindow_active:
                        ev7, vals7 = treeviewWindow.Read()

            if ev3 is None:
                break

            if not loggingWindow_active and ev3 == 'Logging':
                loggingWindow_active = True
                loggedWindow_active = False
                loggedWindow.Hide()

                logs = db.get_log_items()
                table = Sg.Table(logs,
                                 headings=["log id", "evidence_id", "user_id", "session_id", "case_id", "date_time", "title", "details"],
                                 enable_events=True)
                # hides the window loginWindow
                # The layout of the window is created with the 'layout' variable
                layout8 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                           [Sg.Text('', key='OUTPUT')],
                           [Sg.Text('This are all logs')],
                           [table],
                           [Sg.Button('export to csv'), Sg.Button('Ga terug')]]
                # Giving the window the variable layout
                loggingWindow = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout8)

                while True:
                    if loggingWindow_active:
                        ev8, vals8 = loggingWindow.Read()
                        if ev8 == 'export to csv':
                            db.log2csv()
                            print("export")

            if not createCaseWindow_active and ev3 == 'Create Case':
                createCaseWindow_active = True
                loggedWindow.Hide()
                # The layout of the window is created with the 'layout' variable
                layout4 = [[Sg.Text('Case Number: '), Sg.Input()],
                           [Sg.Text('Case Title:      '), Sg.Input('')],
                           [Sg.Text('Case Note:     '), Sg.Input()],
                           [Sg.Button('Back'), Sg.Button('Save Case')]]
                # Giving the window the variable layout
                createCaseWindow = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout4)
                # if the user presses the button create case then a screen will show up with fields that can be
                # filled in
                if createCaseWindow_active and loggedin is True:
                    ev4, vals4 = createCaseWindow.Read()
                    if ev4 == 'Save Case':
                        # giving each variable a value that will save the created case's data in the database
                        x = ev4, vals4[0]
                        number = x[1]
                        y = ev4, vals4[1]
                        title = y[1]
                        z = ev4, vals4[2]
                        note = z[1]
                        # shows a popup that notifies the user that a case has been made
                        makeCase(number, title, note)
                        Sg.Popup('The case: ', title, 'has been made.', icon='ICON.ico')

                        createCaseWindow2_active = True
                        createCaseWindow_active = False
                        createCaseWindow.Hide()
                        # The layout of the window is created with the 'layout' variable
                        layout5 = [[Sg.Radio('E01', "Image", key='E01'), Sg.Radio('RAW', "Image", key='RAW')],
                                   [Sg.Button('Back'), Sg.Button('Save')]]
                        # Giving the window the variable layout
                        createCaseWindow2 = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico')\
                            .Layout(layout5)

                if createCaseWindow2_active:
                    ev5, vals5 = createCaseWindow2.Read()
                    # if the button save is pressed and e01 or raw has been selected, then that image should be possible
                    # to open up
                    if ev5 == 'Save':
                        if vals5['E01']:
                            imageformat = "e01"
                            treeviewWindow_active = True
                            createCaseWindow2_active = False
                            createCaseWindow2.Hide()
                            image = Sg.PopupGetFile('Which image would you like to open?', 'TUF - Choose image')
                            Sg.Popup('The image is being read!')
                            data = Treeview.showfiles(db, image, 'e01')

                            treeview = Sg.Tree(data=data,
                                               headings=['partition_id', 'file_path', 'size', 'extension', 'file_type'],
                                               def_col_width=50)

                            layout7 = [[Sg.Text('Welcome to Turtle Forensics!')],
                                       [treeview],
                                       [Sg.Button("Hash file")],
                                       [Sg.Button("Extract file")],
                                       [Sg.Button("Send to Virustotal")],
                                       [Sg.Button("Wireshark")]]

                            treeviewWindow = Sg.Window('TUF - Treeview', icon='ICON.ico').Layout(layout7)


                            if treeviewWindow_active:
                                ev7, vals7 = treeviewWindow.Read()

                        if vals5['RAW']:
                            imageformat = "raw"
                            treeviewWindow_active = True
                            createCaseWindow2_active = False
                            createCaseWindow2.Hide()
                            image = Sg.PopupGetFile('Which image would you like to open?', 'TUF - Choose image')
                            Sg.Popup('The image is being read!')
                            data = Treeview.showfiles(db, image, 'raw')

                            treeview = Sg.Tree(data=data,
                                               headings=['partition_id', 'file_path', 'size', 'extension', 'file_type'],
                                               def_col_width=50)

                            layout7 = [[Sg.Text('Welcome to Turtle Forensics!')],
                                       [treeview],
                                       [Sg.Button("Hash file")],
                                       [Sg.Button("Extract file")],
                                       [Sg.Button("Send to Virustotal")],
                                       [Sg.Button("Wireshark")]]

                            treeviewWindow = Sg.Window('TUF - Treeview', icon='ICON.ico').Layout(layout7)

                            if treeviewWindow_active:
                                while True:
                                    ev7, vals7 = treeviewWindow.Read()

                                    if ev7 == "Hash file":
                                        file_id = vals7[0]
                                        hash_list = db.get_file_hash(file_id[0])
                                        hash_tuple = hash_list[0]
                                        text = "md5: " + hash_tuple[0] + "\n \n" + "sha256: " + hash_tuple[1] + "\n \n" \
                                               + "sha1: " + hash_tuple[2]
                                        Sg.Popup("File Hash", text)

                                    if ev7 == "Extract file":
                                        file_id = vals7[0]
                                        file_size_list = db.get_file_size(file_id[0])
                                        file_size = file_size_list[0]
                                        if file_size > 0:
                                            filepath_list = db.get_file_path(file_id[0])
                                            partition_offset_list = db.get_partition_offset(file_id[0])
                                            filepath_from_filepath_list = filepath_list[0]
                                            file_name_list = db.get_file_name(file_id[0])
                                            file_name = file_name_list[0]
                                            if imageformat == 'e01':
                                                Image.main.extract_file(image, filepath_from_filepath_list[0], "e01",
                                                    file_name[0], path, partition_offset_list[0])
                                            elif imageformat == 'raw':
                                                Image.main.extract_file(image, filepath_from_filepath_list[0], "raw",
                                                    file_name[0], path, partition_offset_list[0])
                                        else:
                                            Sg.Popup("Extract", "File has no data")

                                    if ev7 == "Send to Virustotal":
                                        # check if api key is set
                                        if virustotal_api == "":
                                            # if not set ask the user
                                            virustotal_api = Sg.PopupGetText('Please provide a VirusTotal API key',
                                                                             'VirusTotal api')
                                            # set the config option to the input given by the user
                                            config.add_section("Virus total")
                                            config['Virus total']['api key'] = virustotal_api
                                            db.log_item(title="Virus total API key opgeslagen",
                                                        details="API key: " + virustotal_api)
                                            # write the config file to config.ini
                                            with open('config.ini', 'w') as configfile:
                                                config.write(configfile)
                                        # get the file_id so the file can be extracted
                                        file_id = vals7[0]
                                        # Extract the file, same as previous window
                                        file_size_list = db.get_file_size(file_id[0])
                                        file_size = file_size_list[0]
                                        if file_size > 0:
                                            filepath_list = db.get_file_path(file_id[0])
                                            partition_offset_list = db.get_partition_offset(file_id[0])
                                            filepath_from_filepath_list = filepath_list[0]
                                            file_name_list = db.get_file_name(file_id[0])
                                            file_name = file_name_list[0]
                                            if imageformat == 'e01':
                                                Image.main.extract_file(image, filepath_from_filepath_list[0], "e01",
                                                    file_name[0], path, partition_offset_list[0])
                                            elif imageformat == 'raw':
                                                Image.main.extract_file(image, filepath_from_filepath_list[0], "raw",
                                                    file_name[0], path, partition_offset_list[0])

                                            vt = VirusTotal.VirusTotal(virustotal_api)

                                            # bestand selecteren
                                            testfile = path + "/" + file_name[0]

                                            # functie test_file uitvoeren
                                            # hier wordt de functie aangeroepen uit de klasse met de constructor
                                            virustotal = vt.test_file(testfile)

                                    if ev7 == "Wireshark":
                                        show_wireshark = Wireshark()

                                        wiresharkdata = show_wireshark.packet2array(
                                            "C:/Users/mzond/Desktop/DEV/TUF/example.pcap")

                                        print(wiresharkdata)
                                        table = Sg.Table(wiresharkdata,
                                                         headings=["                 packet                 "],
                                                         justification='Left',
                                                         )
                                        # hides the window loginWindow
                                        # The layout of the window is created with the 'layout' variable
                                        layout10 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                                                    [Sg.Text('', key='OUTPUT')],
                                                    [Sg.Text('This are all the packkets in the pcap file')],
                                                    [table],
                                                    [Sg.Button('Ga terug')]]
                                        # Giving the window the variable layout
                                        wireshark_window = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(
                                            layout10)
                                        ev10, vals10 = wireshark_window.Read()

                if ev5 is None:
                    break

            # case overview
            if not createCaseWindow2_active and ev3 == 'Open Case' and loggedin is True:
                case = db.get_case(active_case)
                loggedWindow.Hide()
                print(case)
                # The layout of the window is created with the 'layout' variable
                layout5 = [[Sg.Radio('E01', "Image", key='e01'), Sg.Radio('RAW', "Image", key='RAW')],
                           [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                           [Sg.Checkbox('Hash Image after Indexing')],
                           [Sg.Button('Back'), Sg.Button('Save')]]
                # Giving the window the variable layout
                createCaseWindow2 = Sg.Window('Turtle Forensics - case ' + str(case[2]), icon='ICON.ico')\
                    .Layout(layout5)
