if __name__ == '__main__':
    # from lib import GUI as gui
    # from lib import Settings
    from lib import Sqlite

    path = 'C:/Users/Oskar/Desktop/test'
    name = 'test'
    db = Sqlite.Sqlite(path, name)
    db.setup_database()

    def makeCase(number, title, note):
        values = {"number": number, "title": title, "note": note}
        db.set_case(values)

    import PySimpleGUI as Sg

    layout = [[Sg.Text('At which location would you like to save the TUF database?')],
              [Sg.Input(), Sg.FolderBrowse()],
              [Sg.T(' ' * 25), Sg.Button('Yes'), Sg.Button('No')]]
    win1 = Sg.Window('TUF - Turtle Forensics', icon='ICON.ico').Layout(layout)

    win6_active = win5_active = win4_active = win3_active = win2_active = False

    while True:
        ev1, vals1 = win1.Read()

        if ev1 is None:
            break

        if ev1 == 'No':
            break

        if not win2_active and ev1 == 'Yes':
            win2_active = True
            win1.Hide()
            layout2 = [[Sg. Text('Login as a TUF user or create a new user account.')],
                       [Sg.Text('Username'), Sg.Input()],
                       [Sg.Text('Password'), Sg.Input()],
                       [Sg.Button('Login'), Sg.Button('Create User')]]
            win2 = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout2)

        if win2_active:
            ev2, vals2 = win2.Read()

            if ev2 is None:
                break

        if not win3_active and ev2 == 'Create User':
            win3_active = True
            win2.Hide()
            layout3 = [[Sg. Text('Create a new user.')],
                       [Sg.Text('Username'), Sg.Input()],
                       [Sg.Text('Password'), Sg.Input()],
                       [Sg.Button('Create User')]]
            win3 = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout3)

        if win3_active:
            ev3, vals3 = win3.Read()

            if ev3 is None:
                break

            if ev3 == 'Create User':
                if vals3['user'] and ['pass']:
                    db.set_user(vals3)

        if ev3 == 'Create User':
            win3.Close()
            win2_active = True
            win3_active = False
            win2.UnHide()
            ev2, vals2 = win2.Read()

        if not win4_active and ev2 == 'Login':
            win4_active = True
            win2.Hide()
            layout4 = [[Sg.T(' ' * 20), Sg.Text('Welcome to Turtle Forensics!')],
                       [Sg.Text('', key='_OUTPUT_')],
                       [Sg.Text('Would you like to create a new case or open a recent one?')],
                       [Sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(20, 6))],
                       [Sg.Button('Open Case'), Sg.Button('Create Case')]]
            win4 = Sg.Window('TUF - Turtle Forensics', size=(400, 300), icon='ICON.ico').Layout(layout4)

        if win4_active:
            ev4, vals4 = win4.Read()

            if ev4 is None:
                break

        if not win5_active and ev4 == 'Create Case':
            win5_active = True
            win4.Hide()
            layout5 = [[Sg.Text('Case Number: '), Sg.Input()],
                       [Sg.Text('Case Title:      '), Sg.Input('')],
                       [Sg.Text('Case Note:     '), Sg.Input()],
                       [Sg.Button('Back'), Sg.Button('Save Case')]]
            win5 = Sg.Window('Turtle Forensics - Create Case', icon='ICON.ico').Layout(layout5)

        if win5_active:
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
                        print('Hello mijn nama mama')
                    if vals6['RAW']:
                        print('raw')

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
