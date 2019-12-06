import PySimpleGUI as sg

# Type Definition
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# TODO: Determined family only info
family_layout = [sg.Text('Family Type', font='Any 12'),
                 sg.Combo(('Couple', 'PrimarySubscriberAndOneDependent', 'PrimarySubscriberAndTwoDependents',
                           'PrimarySubscriberAndThreeOrMoreDependents',
                           'CoupleAndOneDependent', 'CoupleAndTwoDependents', 'CoupleAndThreeOrMoreDependents'),
                          enable_events=True, key='Family Type', font='Any 12',
                          size=(28, 7))],

# TODO: Medical only
medical_layout = []

# Layout Design
# sg.change_look_and_feel('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Menu(menu_def, tearoff=True)],

          [sg.Text('Healthcare Insurance Database System\n', font=("Helvetica", 16))],

          [sg.Text('State Code', font='Any 12'),
           sg.Combo(('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                     'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                     'NY',
                     'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                     'WI', 'WY'),
                    enable_events=True, key='State', font='Any 12', size=(10, 5)),
           sg.Text("HIOS ID", font='Any 12'), sg.InputText(key='HIOS', size=(20, 1)),
           sg.Text("Plan ID", font='Any 12'), sg.InputText(key='Plan', size=(20, 1))],

          [sg.Text('Insurance Type', font='Any 12'),
           sg.Radio('Dental Only', 'Radio1', default=False, enable_events=True, key='Dental', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Medical', 'Radio1', default=False, enable_events=True, key='Medical', font='Any 12',
                    tooltip='Contains both medical and dental plan', size=(10, 1))],
          [sg.Text('Subscriber Type', font='Any 12'),
           sg.Radio('Individual', 'Radio2', default=False, enable_events=True, key='Individual', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Family', 'Radio2', default=False, enable_events=True, key='Family', font='Any 12', size=(10, 1))],

          [sg.Text('Cover Range', font='Any 12'),
           sg.Radio('Adult-Only', 'Radio3', default=False, enable_events=True, key='Adult', font='Any 12', size=(10, 1)),
           sg.Radio('Child-Only', 'Radio3', default=False, enable_events=True, key='Child', font='Any 12', size=(10, 1)),
           sg.Radio('Adult&Child', 'Radio3', default=False, enable_events=True, key='Adult_Child', font='Any 12',
                       size=(10, 1))],

          [sg.Text('Metal Level', font='Any 12'), sg.Combo(('Platinum', 'Gold', 'Silver', 'Bronze', 'Catastrophic',
                                                            'High(Dental Only Applicable)',
                                                            'Low(Dental Only Applicable)'),
                                                           enable_events=True, key='Metal_Level', font='Any 12',
                                                           size=(18, 7)),
           sg.Text('Monthly Premium', font='Any 12'), sg.Combo(('Lowest', 'Moderate', 'Highest'),
                                                               enable_events=True, key='Monthly_Premium', font='Any 12',
                                                               size=(15, 3))
           ],

          [sg.Text('Maximum Out of Pocket', font='Any 12'), sg.InputText(key='MOOP', size=(9, 1)),
           sg.Text('Primary Subscriber Age', font='Any 12', size=(20, 1)), sg.InputText(key='Age', size=(5, 1))],

          [sg.Frame('Family Only', family_layout, font='Any 12')],

          [sg.Text('Advanced Search Options', font='Any 12')],
          [sg.Checkbox('Wellness Program', default=False, enable_events=True, key='Wellness', font='Any 12',
                       size=(15, 1)),
           sg.Checkbox('Tobacco Usage', default=False, enable_events=True, key='Individual_Tobacco', font='Any 12',
                       size=(12, 1)),
           sg.Checkbox('Pregnancy', default=False, enable_events=True, key='Pregnancy', font='Any 12', size=(10, 1)),
           sg.Checkbox('National Network', default=False, enable_events=True, key='Network', font='Any 11',
                       size=(13, 1)),
           sg.Checkbox('Out of Country', default=False, enable_events=True, key='OutofCountry', font='Any 11',
                       size=(11, 1))],

          [sg.Text('Exchange Preference', font='Any 12'),
           sg.Combo(('On Exchange', 'Off Exchange', 'Both'), enable_events=True, key='Exchange', font='Any 12',
                    size=(10, 3)),
           sg.Text('Disease', font='Any 12'),
           sg.Combo(
               ('Asthma', 'Heart Disease', 'Fracture', 'Diabetes', 'Depression', 'Weight Loss', 'High Blood Pressure',
                'High Cholesterol'), enable_events=True, key='Disease', font='Any 12',
               size=(14, 5))
           ],

          [sg.Text('Copay Preference', font='Any 12'),
           sg.Combo(('No Charge', 'No Charge after deductible', 'Copay with deductible'), enable_events=True,
                    key='Copay', font='Any 12', size=(18, 3)),

           sg.Text('Coinsurance Preference', font='Any 12'),
           sg.Combo(('No Charge', 'No Charge after deductible', 'Fixed %',
                     'Fixed % of Coinsurance after deductible'), enable_events=True, key='Coin', font='Any 12',
                    size=(20, 5))],

          [sg.Button('Search', font='Any 12'), sg.Button('Cancel', font='Any 12')],

          [sg.Text('\n\n\n\n\n\n\nCopyright: Liangbin Zhu, Yujue Wang @ 2019FALL RPI', font=("Helvetica", 8))]]


# ==========================================================================================================
# Implementation function
# Function for processing user interface return values
def values_processing(values):
    pass


# ==========================================================================================================
# Create the Window
window = sg.Window('Insurance Finder', layout, size=(800, 600))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event == 'Search':
        # TODO: Gathering the return values here
        # TODO: Query goes here
        number_result = 1
        result = "CDPHP student plan"
        sg.Popup('Search Results', 'We found %d insurance for you\n%s' % (number_result, result))

window.close()
