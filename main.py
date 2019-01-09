if __name__ == '__main__':
    from lib import GUI as gui
    from lib import Settings
    from lib import Sqlite

    def makecase(x):
        print(x)

    import PySimpleGUI as Sg

    layout = [[Sg.Text('Welcome to Turtle Forensics!')],
              [Sg.Text('', key='_OUTPUT_')],
              [Sg.Text('Would you like to create a new case or open a recent one?')],
              [Sg.T(' ' * 20), Sg.Button('Create Case'), Sg.Button('Open Case')]]

    win1 = Sg.Window('TUF - Turtle Forensics').Layout(layout)

    win4_active = win3_active = win2_active = False

    while True:
        ev1, vals1 = win1.Read()
        # win1.FindElement('_OUTPUT_').Update(vals1[0])
        if ev1 is None or ev1 == 'Exit':
            break

        if not win2_active and ev1 == 'Create Case':
            win2_active = True
            win1.Hide()
            layout2 = [[Sg.Text('Create Case')],
                       [Sg.Text('Case name: '), Sg.Input()],
                       [Sg.Text('Case path: '), Sg.Input('filepath'), Sg.FileBrowse()],
                       [Sg.Button('Save case')],
                       [Sg.Button('Back'), Sg.Button('Next')]]
            win2 = Sg.Window('Create Case').Layout(layout2)

        if win2_active:
            ev2, vals2 = win2.Read()
            if ev2 == 'Save case':
                print(ev2, vals2)
            if ev2 in (None, 'Back', '< Prev'):
                win2_active = False
                win2.Close()
                win1.UnHide()
            elif ev2 == 'Next':
                win3_active = True
                win2_active = False
                win2.Hide()
                layout3 = [[Sg.Radio('E01', "Image"), Sg.Radio('RAW', "Image")],
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






