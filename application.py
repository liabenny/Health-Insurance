import PySimpleGUI as sg

# Type Definition
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# TODO: Determined individual only info
individual_layout = [
    [sg.Text('Text inside of a frame')],
    [sg.Checkbox('Dental Only', default=False, enable_events=True, key='Dental', size=(10, 1)),
     sg.Checkbox('Tobacco Usage', default=False, enable_events=True, key='Individual_Tobacco', size=(10, 1))],
    [sg.Text('Age'), sg.InputText(key='Age', size=(5, 1))],
]

#TODO: Determined family only info
family_layout = []

# Layout Design
sg.change_look_and_feel('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Medical Insurance Finder Database System')],
          [sg.Menu(menu_def, tearoff=True)],
           # TODO: State Code -> Combo
          [sg.Text('Insurance Type'),
           sg.Checkbox('Dental Only', default=False, enable_events=True, key='Dental', size=(10, 1)),
           sg.Checkbox('Medical', default=False, enable_events=True, key='Medical',
                       tooltip='Contains both medical and dental plan', size=(10, 1))],

          [sg.Text('Cover Range'),
           sg.Checkbox('Adult', default=False, enable_events=True, key='Adult', size=(10, 1)),
           sg.Checkbox('Child', default=False, enable_events=True, key='Child', size=(10, 1)),
           sg.Checkbox('Both', default=False, enable_events=True, key='Adult_Child', size=(10, 1))],

          [sg.Text('Metal Level'), sg.Combo(('Platinum', 'Gold', 'Silver', 'Bronze', 'Catastrophic',
                                             'High(Dental Only Applicable)', 'Low(Dental Only Applicable)'),
                                            enable_events=True, key='combo1', size=(15, 3))],
        # TODO: To Be Determined
          [sg.Text('Monthly Premium'), sg.Combo(('Lowest', 'Moderate', 'Highest'),
                                                enable_events=True, key='combo2', size=(15, 3))],

          [sg.Frame('Individual Only', individual_layout, font='Any 11')],
          [sg.Frame('Family Only', family_layout, font='Any 11')],

          [sg.Text('Advanced Search Options')],
          [sg.Checkbox('Exchange', default=False, enable_events=False, key='Exchange', size=(10, 1)),
           sg.Checkbox('Out of Country Coverage', default=False, enable_events=False, key='OutofCountry',
                       size=(10, 1))],
          [sg.Text('Type Preference'), sg.Combo(('Copay', 'Coinsurance'),
                                                enable_events=True, key='combo3', size=(10, 3))],

          [sg.Button('Search'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Insurance Finder', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event == 'Search':
        #TODO: Gathering the return values here
        #TODO: Query goes here
        number_result = 1
        result = "CDPHP student plan"
        sg.Popup('Search Results', 'We found %d insurance for you\n%s' % (number_result, result))

window.close()
