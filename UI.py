import PySimpleGUI as sg

menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

sg.change_look_and_feel('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Medical Insurance Finder Database System')],
          [sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Insurance Type'), sg.Checkbox('Dental Only', default=False, enable_events=False, key = 'Dental', size=(10, 1)),
           sg.Checkbox('Medical', default=False, enable_events=False, size=(10, 1))],
          [sg.Text('Cover Range'), sg.Checkbox('Adult', size=(10, 1)), sg.Checkbox('Child', size=(10, 1)),
           sg.Checkbox('Both', size=(10, 1))],
          [sg.Text('Metal Level'), sg.InputCombo(('Platinum', 'Gold', 'Silver', 'Bronze', 'Catastrophic',
                                                  'High(Dental Only Applicable)', 'Low(Dental Only Applicable)'),
                                                 size=(15, 3))],
          [sg.Text('Advanced Search Options')],
          [sg.Checkbox('Exchange', default=False, enable_events=False, size=(10, 1)),
           sg.Checkbox('Out of Country Coverage', default=False, enable_events=False, size=(10, 1))],
          [sg.Button('Search'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Insurance Finder', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

    sg.Popup('Search Results', 'We found one insurance matches your demand', "CDPHP student plan")

window.close()
