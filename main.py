# main.py
if __name__ == '__main__':
    from lib import GUI as gui
    from lib import Settings
    from lib import Sqlite
    import os
    import PySimpleGUI as Sg

    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    name = 'database'
    db = ''
    loggedin = False
    created = False
    # the currently open case
    active_case = ''


    def makeCase(number, title, note):
        values = {"number": number, "title": title, "note": note}
        db.set_case(values)

    # The layout of the window is created with the 'layout' variable
    layout = [[Sg.Text('At which location would you like to save the TUF database?')],
              [Sg.Input(path), Sg.FolderBrowse()],
              [Sg.T(' ' * 25), Sg.Button('Yes'), Sg.Button('No')]]
    startWindow = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout)

    createCaseWindow2_active = createCaseWindow_active = win4_active = loggedWindow_active = loginWindow_active = False

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
            loginWindow = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout2)

        if loginWindow_active:
            ev2, vals2 = loginWindow.Read()

            if ev2 == "Create User":
                created = False
                username = vals2[0]

                print("creating")

                if ev2 == 'Create User':


                if ev2 is None:
                    break
            else:
                username = vals2[0]
                password = vals2[1]

                if ev2 == 'Login':
                    check_loggedin = db.check_user(username, password)

                    if check_loggedin is True:
                        loggedin = True
                        Sg.Popup("You've been logged in successfully! Welcome " + vals2[0] + "!")
                        break

                    elif check_loggedin is False:
                        loggedin = False
                        Sg.Popup("This combination of username and password does not exist.")
                        ev2, vals2 = loginWindow.Read()

                    else:
                        Sg.Popup("Something went wrong. Try again.")
                        loggedin = False

        if not loggedWindow_active and loggedin is True and created is False:
            cases = db.get_cases()
            table = Sg.Table(cases,
                             headings=["case", "case id", "title", "description", "date created"],
                             enable_events=True)
            loggedWindow_active = True
            loginWindow.Hide()
            # The layout of the window is created with the 'layout' variable
            layout3 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                       [Sg.Text('', key='OUTPUT')],
                       [Sg.Text('Would you like to create a new case or open a recent one?')],
                       [table],
                       [Sg.Button('Open Case'), Sg.Button('Create Case')]]
            loggedWindow = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout3)

            while True:
                if loggedWindow_active:
                    ev3, vals3 = loggedWindow.Read()

                    if ev3 == 'clicked':

                        Sg.Popup(vals3)
                    if ev3 == 'Open Case':
                        active_case = cases[vals3[0][0]][0]
                        break

                    if ev3 is None:
                        break

                if not createCaseWindow_active and ev3 == 'Create Case':
                    createCaseWindow_active = True
                    loggedWindow.Hide()
                    # The layout of the window is created with the 'layout' variable
                    layout4 = [[Sg.Text('Case Number: '), Sg.Input()],
                               [Sg.Text('Case Title:      '), Sg.Input('')],
                               [Sg.Text('Case Note:     '), Sg.Input()],
                               [Sg.Button('Back'), Sg.Button('Save Case')]]
                    createCaseWindow = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout4)

                    if createCaseWindow_active and loggedin is True:
                        ev4, vals4 = createCaseWindow.Read()
                        if ev4 == 'Save Case':
                            x = ev4, vals4[0]
                            number = x[1]
                            y = ev4, vals4[1]
                            title = y[1]
                            z = ev4, vals4[2]
                            note = z[1]

                            makeCase(number, title, note)
                            Sg.Popup('The case: ', title, 'has been made.', icon='ICON.ico')

                            createCaseWindow2_active = True
                            createCaseWindow_active = False
                            createCaseWindow.Hide()
                            # The layout of the window is created with the 'layout' variable
                            layout5 = [[Sg.Radio('E01', "Image", key='E01'), Sg.Radio('RAW', "Image", key='RAW')],
                                       [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                                       [Sg.Checkbox('Hash Image after Indexing')],
                                       [Sg.Button('Back'), Sg.Button('Save')]]
                            createCaseWindow2 = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout5)

                    if createCaseWindow2_active:
                        ev5, vals5 = createCaseWindow2.Read()

                        if ev5 == 'Save':
                            if vals5['E01']:
                                print('e01')
                            if vals5['RAW']:
                                print('raw')

                # case overview
                if not createCaseWindow2_active and ev3 == 'Open Case' and loggedin is True:
                    case = db.get_case(active_case)
                    loggedWindow.Hide()
                    print(case)
                    layout5 = [[Sg.Radio('E01', "Image", key='e01'), Sg.Radio('RAW', "Image", key='RAW')],
                               [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                               [Sg.Checkbox('Hash Image after Indexing')],
                               [Sg.Button('Back'), Sg.Button('Save')]]
                    createCaseWindow2 = Sg.Window('Turtle Forensics - case ' + str(case[2]), icon='ICON.ico').Layout(layout5)

def CreatUser(username, password):
    check_created = db.check_exist(username)

    if check_created == username:
        created = True
        Sg.Popup("This user already exists!")
        ev2, vals2 = loginWindow.Read()

    else:
        db.set_user(values)
        Sg.Popup("The user with the name " + username + " has been created!")
        loggedin = True
        created = False
    break
