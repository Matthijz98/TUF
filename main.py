# main.py
if __name__ == '__main__':
    # from lib import GUI as gui
    # from lib import Settings
    from lib import Sqlite
    import os
    import PySimpleGUI as Sg

    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    name = 'database'
    db = ''
    loggedin = False
    # the currently open case
    active_case = ''

    def makeCase(number, title, note):
        values = {"number": number, "title": title, "note": note}
        db.set_case(values)

# The layout of the window is created with the 'layout' variable
    layout = [[Sg.Text('At which location would you like to save the TUF database?')],
              [Sg.Input(path), Sg.FolderBrowse()],
              [Sg.T(' ' * 25), Sg.Button('Yes'), Sg.Button('No')]]
    win1 = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout)

    win6_active = win5_active = win4_active = win3_active = win2_active = False

    while True:
        ev1, vals1 = win1.Read()
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
        if not win2_active and ev1 == 'Yes':
            win2_active = True
            win1.Hide()
# The layout of the window is created with the 'layout' variable
            layout2 = [[Sg. Text('Login as a TUF user or create a new user account.')],
                       [Sg.Text('Username'), Sg.Input()],
                       [Sg.Text('Password'), Sg.Input(password_char='*')],
                       [Sg.Button('Login'), Sg.Button('Create User')]]
            win2 = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout2)

        if win2_active:
            ev2, vals2 = win2.Read()

            while loggedin is False:
                # If the 'Login' button is pushed the program is going check if the username and password
                # exist in the database.
                if ev2 == 'Login':
                    username = vals2[0]
                    password = vals2[1]
                    check_loggedin = db.check_user(username, password)
# If the username and password are correct then the program is going show a popup screen and go to the next screen.
                    if check_loggedin is True:
                        loggedin = True
                        Sg.Popup("You've been logged in successfully! Welcome " + vals2[0] + "!")
                        break
# If the username and password are incorrect then the program is going show a popup screen and stay on the same window.
                    elif check_loggedin is False:
                        loggedin = False
                        Sg.Popup("This combination of username and password does not exist.")
                        ev2, vals2 = win2.Read()

                    else:
                        Sg.Popup("Something went wrong. Try again.")
                        loggedin = False

                if ev2 == 'Create User':
                    values = [vals2[0], vals2[1]]
                    db.set_user(values)
                    Sg.Popup("The user with the name " + vals2[0] + " has been created!")
                    loggedin = True
                    break

                if ev2 is None:
                    break

        if not win3_active and ev2 == 'Login' and loggedin is True:
            win3_active = True
            win2.Hide()

            cases = db.get_cases()
            table = Sg.Table(cases,
                             headings=["case", "case id", "title", "description", "date created"],
                             enable_events=True)

            layout3 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                       [Sg.Text('', key='_OUTPUT_')],
                       [Sg.Text('Would you like to create a new case or open a recent one?')],
                       [table],
                       [Sg.Button('Open Case'), Sg.Button('Create Case')]]
            win3 = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout3)

            while True:
                if win3_active:
                    win3.Read()

                    if ev3 == 'clicked':
                        Sg.Popup(vals3)

                    if ev3 == 'Open Case':
                        active_case = cases[vals3[0][0]][0]
                        break

                    if ev3 is None:
                        break

        if not win5_active and ev3 == 'Create Case' and loggedin is True:
            win5_active = True
            win3.Hide()
            layout5 = [[Sg.Text('Case Number: '), Sg.Input()],
                       [Sg.Text('Case Title:      '), Sg.Input('')],
                       [Sg.Text('Case Note:     '), Sg.Input()],
                       [Sg.Button('Back'), Sg.Button('Save Case')]]
            win5 = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout5)

        if win5_active and loggedin is True:
            ev5, vals5 = win5.Read()
            if ev5 == 'Save Case':
                x = ev5, vals5[0]
                number = x[1]
                y = ev5, vals5[1]
                title = y[1]
                z = ev5, vals5[2]
                note = z[1]

                makeCase(number, title, note)
                Sg.Popup('The case: ', title, 'has been made.', icon='ICON.ico')

                win6_active = True
                win5_active = False
                win5.Hide()
                layout6 = [[Sg.Radio('E01', "Image", key='e01'), Sg.Radio('RAW', "Image", key='RAW')],
                           [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                           [Sg.Checkbox('Hash Image after Indexing')],
                           [Sg.Button('Back'), Sg.Button('Save')]]
                win6 = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout6)

            if win6_active:
                ev6, vals6 = win6.Read()

                if ev6 == 'Save':
                    if vals6['e01']:
                        print('e01')
                    if vals6['RAW']:
                        print('raw')

        # case overview
        if not win6_active and ev3 == 'Open Case' and loggedin is True:
            case = db.get_case(1)
            win3.Hide()
            print(case)
            layout6 = [[Sg.Radio('E01', "Image", key='e01'), Sg.Radio('RAW', "Image", key='RAW')],
                       [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                       [Sg.Checkbox('Hash Image after Indexing')],
                       [Sg.Button('Back'), Sg.Button('Save')]]
            win6 = Sg.Window('Turtle Forensics - case ' + case[2], icon='ICON.ico').Layout(layout6)


"""           if ev2 in (None, 'Back', '< Prev'):
                win2_active = False
                win2.Close()
                win1.UnHide()
            elif ev3 == 'Next':
                win4_active = True
                win3_active = False
                win3.Hide()
                layout4 = [[Sg.Radio('E01', "Image"), Sg.Radio('RAW', "Image")],
                           [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                           [Sg.Checkbox('Hash Image after Indexing')],
                           [Sg.Button('Back'), Sg.Button('Save')]]
                win3 = Sg.Window('Create Case').Layout(layout3)

        if win3_active:
            ev3, vals3 = win3.Read()
            if ev3 in (None, 'Back', '< Prev'):
                win3.Close()
                win3_active = False
                win2_active = True
                win2.UnHide()
            elif ev3 == 'Save':
                win4_active = True
                win3_active = False
                win3.Hide()
                layout4 = [[Sg.Radio('E01', "Image"), Sg.Radio('RAW', "Image")],
                           [Sg.Text('Image source:    '), Sg.Input(), Sg.FolderBrowse()],
                           [Sg.Checkbox('Hash Image after Indexing')],
                           [Sg.Button('Back'), Sg.Button('Save')]]
                win4 = Sg.Window('Create Case').Layout(layout4)

                if win4_active:
                    ev4, vals4 = win4.Read()
"""
